variable "alicloud_access_key" {
  type        = string
  description = "阿里云 Access Key ID"
}

variable "alicloud_secret_key" {
  type        = string
  description = "阿里云 Access Key Secret"
  sensitive   = true
}


variable "region" {
  type        = string
  description = "阿里云部署地域"
  default     = "cn-shanghai"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC 专有网络网段，例如 172.16.0.0/16"
}

variable "subnet_cidrs" {
  type        = list(string)
  description = "跨可用区交换机（VSwitch）子网网段列表"
}

variable "availability_zones" {
  type        = list(string)
  description = "可用区 ID 列表，例如 [\"cn-shanghai-a\", \"cn-shanghai-b\"]"
}