from grpc import StatusCode


class ServiceException(Exception):
    pass


class ContainerServiceException(ServiceException):
    def __init__(self, status_code: StatusCode, details: str):
        super().__init__(details)
        self.status_code = status_code


class ImageServiceException(ServiceException):
    def __init__(self, status_code: StatusCode, details: str):
        super().__init__(details)
        self.status_code = status_code
