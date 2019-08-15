from storages.backends.s3boto3 import S3Boto3Storage

# 기본 설정값을 오버라이드 하기 위해서 S3Boto3Storage를 상속한다.
class MediaStorage(S3Boto3Storage):
    # 업로드될 버킷
    bucket_name = 'media.dstagram'

    # 업로드될 버킷 하위의 폴더이름
    location = ''

    # 버킷이 존재하는 리전
    region_name = 'ap-northeast-2'

    # 실제로 파일에 접속할 때 사용할 주소
    # 직접 파일을 올려보고 주소를 확인하자.
    custom_domain = 's3.%s.amazonaws.com/%s' % (region_name, bucket_name)
    file_overwrite = False