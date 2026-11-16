# variables.tf
# Declare variables for Terraform configuration
variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "dev"
}


variable "vpcs" {
  description = "List of VPCs to create"
  type        = list(object({
    vpc_name   = string
    cidr_block = string
    subnets    = list(object({
      subnet_name        = string
      cidr_block         = string
      availability_zone  = optional(string, "cn-shanghai-g") # Default to cn-shanghai-g if not provided
    }))
  }))
}

variable "region" {
  type        = string
  description = "阿里云部署地域"
  default     = "cn-shanghai"
}


