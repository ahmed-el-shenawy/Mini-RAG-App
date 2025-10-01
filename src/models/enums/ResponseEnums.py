from enum import Enum


class ResponseSignal(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    FILE_TYPE_INVALID = "invalid_file_type"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_TYPE_VALID = "valid_file_type"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROJECT_CREATION_SUCCESS = "project_creation_success"
    PROJECT_CREATION_FAILED = "project_creation_failed"
    PROJECT_DELETION_SUCCESS = "project_deletion_success"
    PROJECT_DELETION_FAILED = "project_deletion_failed"
