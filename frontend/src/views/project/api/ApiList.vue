<template>
	<section>
		<!--工具条-->
		<el-col :span="24" style="height: 46px">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="名称" @keyup.enter.native="getApiList"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="getApiList">查询</el-button>
				</el-form-item>
				<el-form-item>
					<router-link :to="{ name: '新增接口', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
						<el-button type="primary">新增</el-button>
					</router-link>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" :disabled="update" @click="changeGroup">修改分组</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click.native="DownloadApi">下载接口文档</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click.native="loadSwaggerApi = true">导入接口</el-button>
					<el-dialog title="导入swagger接口" v-model="loadSwaggerApi" :close-on-click-modal="false">
						<el-input v-model="swaggerUrl" placeholder="请输入swagger接口地址" style="width:90%"></el-input>
						<el-button type="primary" @click="addSubmit" :loading="addLoading">导入</el-button>
						<P v-if="!swaggerUrl" style="color: red; margin: 0px">不能为空</P>
					</el-dialog>
				</el-form-item>
			</el-form>
		</el-col>
		<el-dialog title="修改所属分组" v-model="updateGroupFormVisible" :close-on-click-modal="false">
			<el-form :model="updateGroupForm" label-width="80px"  :rules="updateGroupFormRules" ref="updateGroupForm">
				<el-row :gutter="10">
					<el-col :span="12">
						<el-form-item label="父分组" prop="firstGroup">
							<el-select v-model="updateGroupForm.firstGroup" placeholder="请选择" @change="changeSecondGroup">
								<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id">
								</el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="子分组" prop='secondGroup'>
							<el-select v-model="updateGroupForm.secondGroup" placeholder="请选择">
								<el-option v-for="(item,index) in secondGroup" :key="index+''" :label="item.name" :value="item.id"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="updateGroupFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="updateGroupSubmit" :loading="updateGroupLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--列表-->
		<el-table :data="api" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" min-width="5%">
			</el-table-column>
			<el-table-column prop="name" label="接口名称" min-width="17%" sortable show-overflow-tooltip>
				<template slot-scope="scope">
					<el-icon name="name"></el-icon>
					<router-link :to="{ name: '基础信息', params: {api_id: scope.row.id}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
				</template>
			</el-table-column>
			<el-table-column prop="requestType" label="请求方式" min-width="10%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="apiAddress" label="接口地址" min-width="24%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="userUpdate" label="最近更新者" min-width="9%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="lastUpdateTime" label="更新日期" min-width="16%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column label="操作" min-width="19%">
				<template slot-scope="scope">
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
					<router-link :to="{ name: '基础信息', params: {api_id: scope.row.id}}" style='text-decoration: none;color: aliceblue;'>
						<el-button type="info" size="small">修改</el-button>
					</router-link>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :page-count="total" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>

<script>
    import { test } from '../../../api/api'
    import $ from 'jquery'
    export default {
        data() {
            return {
                filters: {
                    name: ''
                },
                api: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列
                updateGroupFormVisible: false,
                updateGroupForm: {
                    firstGroup: "",
                    secondGroup: "",
                },
                updateGroupFormRules: {
                    firstGroup : [{ type: 'number', required: true, message: '请选择父分组', trigger: 'blur'}],
                    secondGroup : [{ type: 'number', required: true, message: '请选择子分组', trigger: 'blur'}]
                },
                group: [],
                secondGroup: [],
                updateGroupLoading: false,
                update: true,
                loadSwaggerApi: false,
                addLoading: false,
                //新增界面数据
                swaggerUrl: "",
            }
        },
        methods: {
            // 获取接口列表
            getApiList() {
                this.listLoading = true;
                let self = this;
                let param = { project_id: this.$route.params.project_id, page: self.page, name: self.filters.name};
                if (this.$route.params.firstGroup) {
                    param['first_group_id'] = this.$route.params.firstGroup;
                    if (this.$route.params.secondGroup) {
                        param['second_group_id'] = this.$route.params.secondGroup
                    }
                }

                $.ajax({
                    type: "get",
                    url: test+"/api/api/api_list",
                    async: true,
                    data: param,
                    headers: {
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    },
                    timeout: 5000,
                    success: function(data) {
                        self.listLoading = false;
                        if (data.code === '999999') {
                            self.total = data.data.total;
                            self.api = data.data.data
                        }
                        else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                    },
                })
            },
            // 修改接口所属分组
            updateGroupSubmit() {
                let ids = this.sels.map(item => item.id).toString();
                let self = this;
                this.$confirm('确认修改所属分组吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.updateGroupLoading = true;
                    //NProgress.start();
                    let params = { project_id:this.$route.params.project_id, first_group_id: self.updateGroupForm.firstGroup, second_group_id: self.updateGroupForm.secondGroup};
                    params['api_ids'] = ids;
                    $.ajax({
                        type: "post",
                        url: test+"/api/api/update_group",
                        async: true,
                        data: params,
                        headers: {
                            Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function(data) {
                            self.updateGroupLoading = false;
                            if (data.code === '999999') {
                                self.$message({
                                    message: '修改成功',
                                    center: true,
                                    type: 'success'
                                })
                            }
                            else {
                                self.$message.error({
                                    message: data.msg,
                                    center: true,
                                })
                            }
                            self.updateGroupFormVisible = false;
                            self.getApiList();
                        },
                    })
                }).catch(() => {

                });
            },
            // 获取api分组
            getApiGroup() {
                let self = this;
                $.ajax({
                    type: "get",
                    url: test+"/api/api/group",
                    async: true,
                    data: { project_id: this.$route.params.project_id},
                    headers: {
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    },
                    timeout: 5000,
                    success: function(data) {
                        if (data.code === '999999') {
                            self.group = data.data;
                            self.updateGroupForm.firstGroup = self.group[0].id
                        }
                        else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                    },
                })
            },
            changeSecondGroup(val) {
                this.secondGroup = [];
                this.updateGroupForm.secondGroup = "";
                for (let i=0; i<this.group.length; i++) {
                    let id = this.group[i]['id'];
                    if ( val === id) {
                        this.secondGroup = this.group[i].secondGroup
                    }
                }
            },
            changeGroup() {
                this.getApiGroup();
                this.updateGroupFormVisible = true

            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    $.ajax({
                        type: "post",
                        url: test+"/api/api/del_api",
                        async: true,
                        data: { project_id: this.$route.params.project_id, api_ids: row.id },
                        headers: {
                            Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function(data) {
                            if (data.code === '999999') {
                                self.$message({
                                    message: '删除成功',
                                    center: true,
                                    type: 'success'
                                })
                            } else {
                                self.$message.error({
                                    message: data.msg,
                                    center: true,
                                })
                            }
                            self.getApiList();
                        },
                    })

                }).catch(() => {
                });
            },
            DownloadApi() {
                $.ajax({
                    type: "get",
                    url: test+"/api/api/Download",
                    async: true,
                    data: { project_id: this.$route.params.project_id},
                    headers: {
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    },
                    timeout: 5000,
                    success: function(data) {
                        if (data.code === "999999") {
                            window.open(test+"/api/api/download_doc?url="+data.data)
                        }
                    },
                })
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getApiList()
            },
            selsChange: function (sels) {
                if (sels.length>0) {
                    this.sels = sels;
                    this.update = false
                } else {
                    this.update = true
                }
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id).toString();
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    $.ajax({
                        type: "post",
                        url: test+"/api/api/del_api",
                        async: true,
                        data:{ project_id: this.$route.params.project_id, api_ids: ids},
                        headers: {
                            Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function(data) {
                            self.listLoading = false;
                            if (data.code === '999999') {
                                self.$message({
                                    message: '删除成功',
                                    center: true,
                                    type: 'success'
                                })
                            }
                            else {
                                self.$message.error({
                                    message: data.msg,
                                    center: true,
                                })
                            }
                            self.getApiList();
                        },
                    })
                }).catch(() => {

                });
            },
			addSubmit(){
                let self = this;
				this.addLoading = true;
				console.log(this.swaggerUrl)
				if (this.swaggerUrl){
				    $.ajax({
                        type: "post",
                        url: test+"/api/api/lead_swagger",
                        async: true,
                        data:{ project_id: this.$route.params.project_id, url: this.swaggerUrl},
                        headers: {
                            Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function(data) {
                            if (data.code === '999999') {
                                self.$message({
                                    message: '添加成功',
                                    center: true,
                                    type: 'success'
                                });
                                self.listLoading = true;
                                self.addLoading = false;
                                self.loadSwaggerApi = false;
                                self.getApiList()
                            }
                            else {
                                self.addLoading = false;
                                self.$message.error({
                                    message: "导入失败，请检查地址是否正确",
                                    center: true,
                                })
                            }
                            self.getApiList();
                        },
                    })
				} else {
				    this.addLoading = false
				}
			},
        },
        mounted() {
            this.getApiList();

        }
    }
</script>

<style lang="scss" scoped>
	.api-title {
		padding: 15px;
		margin: 0px;
		text-align: center;
		border-radius:5px;
		font-size: 15px;
		color: aliceblue;
		background-color: rgb(32, 160, 255);
		font-family: PingFang SC;
	}
	.group .editGroup {
		float:right;
	}
	.row-title {
		margin: 35px;
	}
	.addGroup {
		margin-top: 0px;
		margin-bottom: 10px;
		border-radius: 25px;
	}
	.api-view-a {
		margin-left: 15px;
		margin-right: 15px;
		display: block;
	}
	.api-view-b {
		margin-left: 15px;
		margin-right: 15px;
		display: none;
	}
</style>