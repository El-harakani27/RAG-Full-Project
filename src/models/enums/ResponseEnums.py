from enum import Enum
class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validated_success"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOADED_SUCCESS = "file_upload_success"
    FILE_UPLOADED_FAILD = "file_uplaod_faild"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESS = "processing_success"
    NO_FILES_ERROR = "No_Files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
