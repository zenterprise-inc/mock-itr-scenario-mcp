# Mock ITR Scenario MCP Server

Mock ItrLoader 프로젝트의 시나리오를 생성하고 관리하는 MCP(Model Context Protocol) 서버입니다.

## 기능

### MCP Tools

#### 기본 도구

| 도구 | 설명 |
|------|------|
| `template_list` | 사용 가능한 시나리오 템플릿 목록 조회 |
| `template_load` | 특정 템플릿 로드 |
| `scenario_build_normal` | 정상 환급 시나리오 생성 |
| `scenario_build_error` | 에러 시나리오 생성 |
| `scenario_build_progress` | 진행률 전송 시나리오 생성 |
| `scenario_validate` | 시나리오 유효성 검사 |
| `scenario_assign` | 시나리오를 user_ern에 할당 |
| `scenario_unassign` | 시나리오 할당 해제 |
| `error_types_list` | 지원하는 에러 타입 목록 조회 |

#### Flow별 시나리오 생성 도구

| 도구 | 설명 | Flow |
|------|------|------|
| `scenario_build_simple_auth` | [개인] 간편인증 flow 시나리오 생성 | cert_request → cert_response → check → load |
| `scenario_build_common_cert` | [개인] 공동인증서 flow 시나리오 생성 | check (common_cert) → load |
| `scenario_build_corp_common_cert` | [법인] 공동인증서 또는 ID/PW flow 시나리오 생성 | corp_check (common_cert 또는 id/pw) → corp_load_calc |

#### 실패 시나리오 생성 도구

| 도구 | 설명 |
|------|------|
| `scenario_build_simple_auth_fail` | 간편인증 요청(cert_request) 실패 시나리오 생성 |
| `scenario_build_cert_response_fail` | 간편인증 완료 확인(cert_response) 실패 시나리오 생성 |

### MCP Resources

| 리소스 | 설명 |
|--------|------|
| `scenario://templates` | 템플릿 목록 |
| `scenario://error-types` | 지원하는 에러 타입 목록 |
| `scenario://schema` | 시나리오 JSON Schema |

## 설치

### uv 설치

uv가 설치되어 있지 않다면 다음 명령으로 설치할 수 있습니다.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 macOS/Homebrew
brew install astral-sh/uv/uv
# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

```bash
# uv 사용
uv pip install -e .

# pip 사용
pip install -e .
```

### GitHub에서 MCP 서버 가져오기 및 등록 절차

1. **GitHub 저장소 포크**
   - 원본(Upstream): `https://github.com/danny-zent/mock-itr-scenario-mcp`
   - 조직 또는 개인 GitHub 계정으로 Fork를 생성합니다.
2. **포크한 저장소 클론**
   ```bash
   git clone https://github.com/<your-org-or-id>/mock-itr-scenario-mcp.git
   cd mock-itr-scenario-mcp
   ```
3. **의존성 설치** (위 `설치` 절차 참고)
3. **MCP 서버 경로 확인**  
   - `command`: `uv`  
   - `args`: `["run", "-m", "mock_itr_scenario_mcp.server"]`  
   - `cwd`: 클론한 저장소 경로 (예: `/Users/danny/git/mock-itr-scenario-mcp`)
4. **Cursor / Claude 설정 파일에 mcpServers 항목 추가**  
   - Cursor: `~/.cursor/mcp.json`  
   - Claude Desktop: `claude_desktop_config.json`  
   - 아래 예시처럼 `mcpServers.mock-itr-scenario` 블록을 추가하고 환경변수를 원하는 값으로 세팅
5. **에디터 재시작 또는 MCP 서버 새로 고침**  
   - Cursor: `⌘K` → “Reload MCP Servers”  
   - Claude Desktop: 설정 저장 후 앱 재시작

## 사용법

### Cursor 설정

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mock-itr-scenario": {
      "command": "uv",
      "args": ["run", "-m", "mock_itr_scenario_mcp.server"],
      "cwd": "/Users/you/path/to/your-fork/mock-itr-scenario-mcp",
      "env": {
        "MOCK_ITR_MODEL_YEAR": "2024",
        "DYNAMODB_ENDPOINT_URL": "http://localhost:8000"
      }
    }
  }
}
```

### Claude Desktop 설정

`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mock-itr-scenario": {
      "command": "uv",
      "args": ["run", "-m", "mock_itr_scenario_mcp.server"],
      "cwd": "C:/Users/you/path/to/your-fork/mock-itr-scenario-mcp",
      "env": {
        "MOCK_ITR_MODEL_YEAR": "2024"
      }
    }
  }
}
```

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `MOCK_ITR_MODEL_YEAR` | 귀속연도 (attr_yr) | `2024` |
| `DYNAMODB_ENDPOINT_URL` | DynamoDB 엔드포인트 URL | (AWS 기본) |
| `SCENARIO_TABLE_NAME` | DynamoDB 테이블 이름 | `mock-itr-scenarios` |
| `AWS_REGION` | AWS 리전 | `ap-northeast-2` |

## 사용 예시

### 템플릿 목록 조회

템플릿은 프로젝트 루트의 `templates/` 디렉토리에 `TPL_*.json` 형식으로 저장됩니다.

```
사용자: "사용 가능한 템플릿 목록 보여줘"

AI: template_list 도구를 사용합니다.

사용 가능한 템플릿:
- TPL_NORMAL_BIZ_HIGH: 개인사업자 고액환급 (5,500,000원)
- TPL_NORMAL_BIZ_LOW: 개인사업자 저액환급 (150,000원)
- TPL_ERR_NO_TAX_RETURN: 종소세신고내역없음 에러
...
```

### 시나리오 생성

#### 기본 시나리오 생성 (로그인 방식 선택 가능)

```
사용자: "300만원 환급 시나리오 만들어줘"

AI: scenario_build_normal 도구를 사용합니다.

생성된 시나리오:
- 사용자: 테스트사용자
- 환급액: 3,000,000원
- 사업자 유형: 개인사업자
- 로그인 방식: 간편인증 (기본값)
```

#### 로그인 방식 지정

**개인 - 간편인증 (카카오/네이버)**
```
사용자: "간편인증(네이버)으로 300만원 환급 시나리오 만들어줘"

AI: scenario_build_normal 도구를 사용합니다 (login_method: simple_auth, cert_type: naver).

생성된 시나리오:
- Flow: cert_request → cert_response → check → load
- 간편인증: 네이버
- 환급액: 3,000,000원
```

**개인 - 공동인증서**
```
사용자: "공동인증서로 300만원 환급 시나리오 만들어줘"

AI: scenario_build_normal 도구를 사용합니다 (login_method: common_cert).

생성된 시나리오:
- Flow: check (common_cert) → load
- 환급액: 3,000,000원
```

**법인 - 공동인증서**
```
사용자: "법인 공동인증서로 시나리오 만들어줘"

AI: scenario_build_normal 도구를 사용합니다 (biz_type: corp, login_method: corp_common_cert).

생성된 시나리오:
- Flow: corp_check (common_cert) → corp_load_calc
- 사업자 유형: 법인
```

**법인 - ID/PW**
```
사용자: "법인 ID/PW로 시나리오 만들어줘"

AI: scenario_build_normal 도구를 사용합니다 (biz_type: corp, login_method: corp_id_pw).

생성된 시나리오:
- Flow: corp_check (id/pw) → corp_load_calc
- 사업자 유형: 법인
- 로그인 방식: ID/PW
```

### Flow별 시나리오 생성

#### 간편인증 Flow (개인)

```
사용자: "카카오 간편인증으로 500만원 환급 시나리오 만들어줘"

AI: scenario_build_simple_auth 도구를 사용합니다.

생성된 시나리오:
- Flow: cert_request → cert_response → check → load
- 사용자: 테스트사용자
- 간편인증: 카카오
- 환급액: 5,000,000원
```

#### 공동인증서 Flow (개인)

```
사용자: "공동인증서로 200만원 환급 시나리오 만들어줘"

AI: scenario_build_common_cert 도구를 사용합니다.

생성된 시나리오:
- Flow: check (common_cert) → load
- 환급액: 2,000,000원
```

#### 공동인증서 Flow (법인)

```
사용자: "법인 공동인증서 시나리오 만들어줘"

AI: scenario_build_corp_common_cert 도구를 사용합니다.

생성된 시나리오:
- Flow: corp_check (common_cert) → corp_load_calc
- 사업체명: 주식회사 테스트사업자
- 로그인 방식: 공동인증서
```

#### ID/PW Flow (법인)

```
사용자: "법인 ID/PW 시나리오 만들어줘"

AI: scenario_build_corp_common_cert 도구를 사용합니다 (login_method: corp_id_pw).

생성된 시나리오:
- Flow: corp_check (id/pw) → corp_load_calc
- 사업체명: 주식회사 테스트사업자
- 로그인 방식: ID/PW
- 홈택스 ID/PW 사용
```

### 실패 시나리오 생성

#### 간편인증 요청 실패

```
사용자: "카카오 간편인증 요청 실패 시나리오 만들어줘"

AI: scenario_build_simple_auth_fail 도구를 사용합니다.

생성된 시나리오:
- cert_request: 실패
- 에러 타입: 간편인증오류
- 에러 메시지: "카카오톡 간편인증 요청에 실패했습니다. 사용자 정보를 확인해주세요."
```

#### 간편인증 완료 확인 실패

```
사용자: "간편인증 완료 확인 실패 시나리오 만들어줘"

AI: scenario_build_cert_response_fail 도구를 사용합니다.

생성된 시나리오:
- cert_request: 성공
- cert_response: 실패
- 에러 타입: 간편인증미완료
- 에러 메시지: "간편인증이 완료되지 않았습니다."
```

### 에러 시나리오 생성

#### 기환급자 에러

```
사용자: "기환급자 에러 시나리오 만들어줘"

AI: scenario_build_error 도구를 사용합니다.

생성된 시나리오:
- 에러 타입: 기환급자
- 발생 액션: load
- 에러 메시지: "2024" (환경변수 MOCK_ITR_MODEL_YEAR 값)
- 설명: 같은 귀속년도에 이미 환급을 받은 사람이 다시 조회(load) 액션을 할 때 발생
```

#### 종소세 신고내역 없음 에러

```
사용자: "종소세 신고내역 없음 에러 시나리오 만들어줘"

AI: scenario_build_error 도구를 사용합니다.

생성된 시나리오:
- 에러 타입: 종소세신고내역없음
- 에러 메시지: "종합소득세 신고 내역이 없습니다."
```

## 개발

```bash
# 개발 의존성 설치
uv pip install -e ".[dev]"

# 테스트 실행
pytest

# 린트
ruff check .

# 타입 체크
mypy src
```

## 시나리오 데이터 구조

### 액션별 요청/응답 데이터

각 시나리오 액션은 [Confluence 문서의 API 스펙](https://zenterprise.atlassian.net/wiki/spaces/BN2022/pages/4266000430/API)에 맞춰 요청/응답 데이터 구조를 포함합니다:

- **cert_request**: 간편인증 요청 (user_info 기반)
- **cert_response**: 간편인증 완료 확인 (user_info + cert_info 기반)
- **check**: 사용자 검증 (token 또는 common_cert 기반, tin/cookies 반환)
- **load**: 수집 및 계산 (cookies 기반, 환급 결과 반환)
- **calc**: 계산 (export_file_prefix 기반)
- **corp_load_calc**: 법인 수집 및 계산 (cookies 기반)

### Flow 설명

#### 1. [개인] 간편인증 Flow
```
사용자정보입력 → cert_request → 사용자 인증완료 → cert_response → check (token) → load
```
- **로그인 방식**: `simple_auth`
- **간편인증 유형**: `kakao` 또는 `naver`
- **액션 순서**: cert_request → cert_response → check → load

#### 2. [개인] 공동인증서 Flow
```
인증서정보 → check (common_cert) → load
```
- **로그인 방식**: `common_cert`
- **액션 순서**: check → load

#### 3. [법인] 공동인증서 Flow
```
인증서정보 → corp_check (common_cert) → corp_load_calc
```
- **로그인 방식**: `corp_common_cert`
- **액션 순서**: corp_check → corp_load_calc

#### 4. [법인] ID/PW Flow
```
홈택스 ID/PW → corp_check (id/pw) → corp_load_calc
```
- **로그인 방식**: `corp_id_pw`
- **액션 순서**: corp_check → corp_load_calc
- **필수 파라미터**: `id`, `pw`, `resno` (주민번호 앞7자리)

### 로그인 방식 선택 가이드

#### 개인 로그인 방식
- **간편인증서 (`simple_auth`)**: 카카오톡 또는 네이버 간편인증 사용
  - `cert_type`: `kakao` 또는 `naver`
  - Flow: cert_request → cert_response → check → load
- **공동인증서 (`common_cert`)**: 공동인증서 사용
  - Flow: check → load

#### 법인 로그인 방식
- **공동인증서 (`corp_common_cert`)**: 공동인증서 사용
  - Flow: corp_check → corp_load_calc
- **ID/PW (`corp_id_pw`)**: 홈택스 ID/PW 사용
  - Flow: corp_check → corp_load_calc
  - 필수 파라미터: `id`, `pw`, `resno`

### 주요 에러 타입

#### 기환급자 (ALREADY_REFUNDED)
- **발생 액션**: `load`
- **설명**: 같은 귀속년도에 이미 환급을 받은 사람이 다시 조회(load) 액션을 할 때 발생
- **에러 메시지**: 환경변수 `MOCK_ITR_MODEL_YEAR`의 값 (예: "2024", "2025")
- **예시**: 2024년에 이미 환급을 받은 사용자가 2024년 환급을 다시 조회하려고 할 때 발생

#### 사업자없음오류 (NO_BIZ)
- **발생 액션**: `load`
- **설명**: 홈택스 계정에 사업자가 없음
- **에러 메시지**: "처리중 예외가 발생하였습니다. [ 사업자 변경대상이 아님 ]"

#### 세션만료 (SESSION_EXPIRED)
- **발생 액션**: `load`
- **설명**: 수집 중 세션 만료 (재시도 필요)
- **에러 메시지**: "중복접속으로 세션이 만료되었습니다."

#### 주민번호오류 (INVALID_SSN)
- **발생 액션**: `load`
- **설명**: 주민등록번호 오류로 인한 수집 실패
- **에러 메시지**: "사업자등록번호/주민등록번호을(를) 확인하세요."

## 참고 자료

- [Mock ItrLoader](https://github.com/danny-zent/mock-itrLoader)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [비즈넵 환급 세액 계산 람다 API 가이드](https://zenterprise.atlassian.net/wiki/spaces/BN2022/pages/4266000430/API)
