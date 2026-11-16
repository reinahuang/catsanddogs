# ==========================================
# 1. 管理员角色 (Admin Role - 具备 Root 级管理权限)
# ==========================================
data "alicloud_ram_policy_document" "admin_trust_ds" {
  statement {
    effect  = "Allow"
    action  = ["sts:AssumeRole"]
    principal {
      entity = "RAM"
      identifiers = [
        # 允许当前主账号下的可信实体扮演此角色
        "acs:ram::${data.alicloud_account.current.id}:root"
      ]
    }
  }
}

resource "alicloud_ram_role" "admin_role" {
  role_name                   = "tf-lab-ecs-admin-role"
  description                 = "Terraform 最高管理员角色，用于 Assume Role 提权部署"
  assume_role_policy_document = data.alicloud_ram_policy_document.admin_trust_ds.document
}

resource "alicloud_ram_role_policy_attachment" "admin_attach" {
  policy_name = "AdministratorAccess"
  policy_type = "System"
  role_name   = alicloud_ram_role.admin_role.role_name
}

# ==========================================
# 2. 查询 ECS 免密服务角色 (ECS Service Role)
# ==========================================
data "alicloud_ram_policy_document" "ecs_trust_ds" {
  statement {
    effect  = "Allow"
    action  = ["sts:AssumeRole"]
    principal {
      entity      = "Service"
      identifiers = ["ecs.aliyuncs.com"]
    }
  }
}

resource "alicloud_ram_role" "ecs_role" {
  role_name                   = "tf-lab-ecs-role"
  description                 = "允许 ECS 实例免密调用 API访问alicloud的角色"
  assume_role_policy_document = data.alicloud_ram_policy_document.ecs_trust_ds.document
}

resource "alicloud_ram_role_policy_attachment" "ecs_attach" {
  policy_name = "AliyunVPCReadOnlyAccess"
  policy_type = "System"
  role_name   = alicloud_ram_role.ecs_role.role_name
}

# ==========================================
# 3. GitOps 自动化服务账号 (RAM User)
# ==========================================
resource "alicloud_ram_user" "sa_automation" {
  name         = "sa-gitops-pipeline"
  display_name = "GitOps Automation Service Account"
  comments     = "用于 GitHub Actions等CICD自动部署基础设施的 Service Account"
}

resource "alicloud_ram_access_key" "sa_ak" {
  user_name = alicloud_ram_user.sa_automation.name
  description = "管理访问控制（RAM）的权限，即管理用户以及授权的权限"
  policy_name = "AliyunRAMFullAccess"
}

resource "alicloud_ram_user_policy_attachment" "sa_attach" {
  policy_name = "AliyunVPCFullAccess"
  policy_type = "System"
  user_name   = alicloud_ram_user.sa_automation.name
  description = "管理专有网络（VPC）的权限"
}