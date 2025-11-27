"""Scenario configuration models."""

from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from .enums import BizType, CertType


class UserInfo(BaseModel):
    """사용자 정보"""
    name: str = Field(default="테스트사용자", description="사용자 이름")
    phone: str = Field(default="01012345678", description="전화번호")
    birthday: str = Field(default="19900101", description="생년월일 (YYYYMMDD)")
    cert_type: str | None = Field(default=None, description="간편인증 유형 (cert_request에서 사용)")


class TaxpayerInfo(BaseModel):
    """납세자 정보"""
    tin: str = Field(default="123456789012345678", description="납세자관리번호 (18자리)")
    tax_office_code: str = Field(default="123", description="관할세무서코드")
    tax_office_name: str = Field(default="강남세무서", description="관할세무서명")


def get_default_model_year() -> str:
    """환경변수에서 귀속연도 가져오기 (기본값: 2024)"""
    import os
    return os.environ.get("MOCK_ITR_MODEL_YEAR", "2024")


class MetaInfo(BaseModel):
    """메타 정보"""
    client_id: str = Field(default="bznav-refund-mock", description="클라이언트 ID")
    model_year: str = Field(default_factory=get_default_model_year, description="귀속연도")


class CertInfo(BaseModel):
    """인증 정보"""
    cert_type: CertType = Field(default=CertType.KAKAO, description="간편인증 유형")
    tx_id: str = Field(default="", description="간편인증 트랜잭션 ID")
    req_tx_id: str = Field(default="", description="요청 트랜잭션 ID")
    token: str = Field(default="", description="인증 토큰")
    cx_id: str = Field(default="", description="CX ID")


class CommonCert(BaseModel):
    """공동인증서 정보"""
    sign_cert: str = Field(default="", description="공동인증서 공개키 (base64)")
    sign_pri: str = Field(default="", description="공동인증서 개인키 (base64)")
    sign_pw: str = Field(default="", description="공동인증서 비밀번호")


class Cookies(BaseModel):
    """쿠키 정보"""
    nts_login_system_code_p: str = Field(default="TXPP", description="NTS 로그인 시스템 코드")
    txpp_session_id: str = Field(default="", description="TXPP 세션 ID")


# ============================================================================
# 액션별 요청/응답 데이터 모델
# ============================================================================

class CertRequestRequest(BaseModel):
    """cert_request 요청 데이터"""
    action: str = Field(default="cert_request", description="액션 타입")
    user_info: UserInfo = Field(description="사용자 정보")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")


class CertRequestResponse(BaseModel):
    """cert_request 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, str] = Field(default_factory=dict, description="reqTxId, token, cxId")


class CertResponseRequest(BaseModel):
    """cert_response 요청 데이터"""
    action: str = Field(default="cert_response", description="액션 타입")
    user_info: UserInfo = Field(description="사용자 정보")
    cert_info: CertInfo = Field(description="인증 정보")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")


class CertResponseResponse(BaseModel):
    """cert_response 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, str] = Field(default_factory=dict, description="token 등 인증 결과")


class CheckRequest(BaseModel):
    """check 요청 데이터"""
    action: str = Field(default="check", description="액션 타입")
    id: str = Field(default="", description="홈택스 아이디")
    pw: str = Field(default="", description="홈택스 비밀번호")
    token: str = Field(default="", description="간편인증 토큰 (cert_response에서 받은 token)")
    common_cert: CommonCert | None = Field(default=None, description="공동인증서 정보")
    cookies: dict[str, Any] | None = Field(default=None, description="로그인 쿠키 정보")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")


class CheckResponse(BaseModel):
    """check 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, Any] = Field(default_factory=dict, description="tin, cookies")


class LoadRequest(BaseModel):
    """load 요청 데이터"""
    action: str = Field(default="load", description="액션 타입")
    id: str = Field(default="", description="홈택스 아이디")
    pw: str = Field(default="", description="홈택스 비밀번호")
    token: str = Field(default="", description="간편인증 토큰")
    cookies: dict[str, Any] | None = Field(default=None, description="로그인 쿠키 정보")
    reg_no: str = Field(default="", description="입력받은 주민번호")
    export_file_prefix: str = Field(default="", description="파일 접두사 (기본값: tin)")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")
    use_sqs: bool = Field(default=False, description="SQS 전송 여부")
    corp_type: str = Field(default="", description="사업형태 (INDIS/CORPS)")
    tin: str = Field(default="", description="납세자번호")
    send_next_step: bool = Field(default=True, description="다음 액션 실행 여부")


class LoadResponse(BaseModel):
    """load 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, Any] = Field(default_factory=dict, description="수집/계산 결과 데이터")


class CalcRequest(BaseModel):
    """calc 요청 데이터"""
    action: str = Field(default="calc", description="액션 타입")
    export_file_prefix: str = Field(description="파일 접두사")
    model_year: str = Field(default="", description="귀속연도")
    survey_contents: dict[str, Any] | None = Field(default=None, description="터칭콜설문 내용")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")
    calc_version: str = Field(default="latest", description="모델버전")


class CalcResponse(BaseModel):
    """calc 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, Any] = Field(default_factory=dict, description="계산 결과 데이터")


class CorpCheckRequest(BaseModel):
    """corp_check 요청 데이터"""
    action: str = Field(default="corp_check", description="액션 타입")
    id: str = Field(default="", description="홈택스 아이디")
    pw: str = Field(default="", description="홈택스 비밀번호")
    resno: str = Field(default="", description="주민번호 앞7자리")
    common_cert: CommonCert | None = Field(default=None, description="공동인증서 정보")
    cookies: dict[str, Any] | None = Field(default=None, description="로그인 쿠키 정보")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")


class CorpCheckResponse(BaseModel):
    """corp_check 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, Any] = Field(default_factory=dict, description="법인 정보 (구분, 사업체명, 사업자번호, 대표자명, tin, cookies)")


class CorpLoadCalcRequest(BaseModel):
    """corp_load_calc 요청 데이터"""
    action: str = Field(default="corp_load_calc", description="액션 타입")
    cookies: dict[str, Any] | None = Field(default=None, description="로그인 쿠키 정보 (check에서 받은 cookies)")
    export_file_prefix: str = Field(default="", description="파일 접두사 (기본값: tin)")
    user_ern: str = Field(default="", description="추적용 사용자 ERN")
    use_sqs: bool = Field(default=False, description="SQS 전송 여부")
    tin: str = Field(default="", description="납세자번호")


class CorpLoadCalcResponse(BaseModel):
    """corp_load_calc 응답 데이터"""
    error: dict[str, Any] = Field(default_factory=lambda: {"status": False, "type": "", "msg": ""})
    result: dict[str, Any] = Field(default_factory=dict, description="법인 수집/계산 결과 데이터")


class ActionConfig(BaseModel):
    """액션별 설정"""
    success: bool = Field(default=True, description="성공 여부")
    delay_seconds: float = Field(default=0.0, description="응답 지연 시간 (초)")
    error_type: str | None = Field(default=None, description="에러 타입")
    error_msg: str | None = Field(default=None, description="에러 메시지")
    extra_data: dict[str, Any] | None = Field(default=None, description="추가 데이터")
    request_data: dict[str, Any] | None = Field(default=None, description="요청 데이터 (액션별 요청 모델 구조)")
    response_data: dict[str, Any] | None = Field(default=None, description="응답 데이터 (액션별 응답 모델 구조)")


class ProgressStep(BaseModel):
    """진행률 단계"""
    step_name: str = Field(description="단계 이름")
    progress: str = Field(description="진행률 (예: '20%')")
    delay_seconds: float = Field(default=0.5, description="지연 시간")


class ProgressConfig(BaseModel):
    """진행률 설정"""
    enabled: bool = Field(default=False, description="진행률 전송 활성화")
    queue_name: str = Field(default="refund-search.fifo", description="SQS 큐 이름")
    steps: list[ProgressStep] = Field(default_factory=list, description="진행률 단계")


class RefundItem(BaseModel):
    """환급 항목"""
    name: str = Field(description="항목명")
    amount: int = Field(default=0, description="금액")


class BizLocation(BaseModel):
    """사업장 정보"""
    biz_no: str = Field(default="", description="사업자번호")
    biz_name: str = Field(default="", description="상호")
    address: str = Field(default="", description="주소")


class RefundResult(BaseModel):
    """환급 결과"""
    total_refund: int = Field(default=0, description="총 환급세액")
    refund_items: list[RefundItem] = Field(default_factory=list, description="환급 항목 목록")
    biz_locations: list[BizLocation] = Field(default_factory=list, description="사업장 목록")
    
    # 세부 환급 항목 (레거시 호환)
    창중감_환급액: int = Field(default=0, alias="창중감_환급액")
    고용증대_환급액: int = Field(default=0, alias="고용증대_환급액")
    사회보험료_환급액: int = Field(default=0, alias="사회보험료_환급액")
    중소기업특별세액_환급액: int = Field(default=0, alias="중소기업특별세액_환급액")
    양도세_환급액: int = Field(default=0, alias="양도세_환급액")
    
    model_config = ConfigDict(populate_by_name=True)


class VersionInfo(BaseModel):
    """버전 정보"""
    gcexcel_version: str = Field(default="1.0.0", description="GCExcel 버전")
    itrloader_version: str = Field(default="1.0.0", description="ItrLoader 버전")


class ScenarioConfig(BaseModel):
    """시나리오 설정"""
    # 메타데이터
    scenario_id: str = Field(default="", description="시나리오 ID")
    scenario_name: str = Field(default="", description="시나리오 이름")
    description: str = Field(default="", description="시나리오 설명")
    
    # 사용자/납세자 정보
    user_info: UserInfo = Field(default_factory=UserInfo, description="사용자 정보")
    taxpayer_info: TaxpayerInfo = Field(default_factory=TaxpayerInfo, description="납세자 정보")
    cert_info: CertInfo = Field(default_factory=CertInfo, description="인증 정보")
    meta_info: MetaInfo = Field(default_factory=MetaInfo, description="메타 정보")
    
    # 사업자 유형 및 환급 결과
    biz_type: BizType = Field(default=BizType.INDIVIDUAL_BIZ, description="사업자 유형")
    refund_result: RefundResult = Field(default_factory=RefundResult, description="환급 결과")
    
    # 버전 정보
    version_info: VersionInfo = Field(default_factory=VersionInfo, description="버전 정보")
    
    # 액션별 설정
    cert_request_config: ActionConfig = Field(default_factory=ActionConfig, description="cert_request 설정")
    cert_response_config: ActionConfig = Field(default_factory=ActionConfig, description="cert_response 설정")
    check_config: ActionConfig = Field(default_factory=ActionConfig, description="check 설정")
    load_config: ActionConfig = Field(default_factory=ActionConfig, description="load 설정")
    calc_config: ActionConfig = Field(default_factory=ActionConfig, description="calc 설정")
    corp_check_config: ActionConfig = Field(default_factory=ActionConfig, description="corp_check 설정")
    corp_load_calc_config: ActionConfig = Field(default_factory=ActionConfig, description="corp_load_calc 설정")
    
    # 진행률 설정
    progress_config: ProgressConfig = Field(default_factory=ProgressConfig, description="진행률 설정")
    
    def to_dict(self) -> dict[str, Any]:
        """딕셔너리로 변환"""
        return self.model_dump(by_alias=True, exclude_none=True)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScenarioConfig":
        """딕셔너리에서 생성"""
        return cls.model_validate(data)
