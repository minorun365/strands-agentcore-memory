 → cd backend
pip install strands-agents==1.0.1 bedrock-agentcore==0.1.0 bedrock-agentcore-starter-toolkit==0.1.1
agentcore --version

Collecting strands-agents==1.0.1
  Downloading strands_agents-1.0.1-py3-none-any.whl.metadata (12 kB)
Collecting bedrock-agentcore==0.1.0
  Downloading bedrock_agentcore-0.1.0-py3-none-any.whl.metadata (5.2 kB)
Collecting bedrock-agentcore-starter-toolkit==0.1.1
  Downloading bedrock_agentcore_starter_toolkit-0.1.1-py3-none-any.whl.metadata (6.2 kB)
Collecting boto3<2.0.0,>=1.26.0 (from strands-agents==1.0.1)
  Downloading boto3-1.39.14-py3-none-any.whl.metadata (6.7 kB)
Collecting botocore<2.0.0,>=1.29.0 (from strands-agents==1.0.1)
  Downloading botocore-1.39.14-py3-none-any.whl.metadata (5.7 kB)
Collecting docstring-parser<1.0,>=0.15 (from strands-agents==1.0.1)
  Downloading docstring_parser-0.17.0-py3-none-any.whl.metadata (3.5 kB)
Collecting mcp<2.0.0,>=1.8.0 (from strands-agents==1.0.1)
  Downloading mcp-1.12.2-py3-none-any.whl.metadata (60 kB)
Collecting opentelemetry-api<2.0.0,>=1.30.0 (from strands-agents==1.0.1)
  Downloading opentelemetry_api-1.35.0-py3-none-any.whl.metadata (1.5 kB)
Collecting opentelemetry-instrumentation-threading<1.00b0,>=0.51b0 (from strands-agents==1.0.1)
  Downloading opentelemetry_instrumentation_threading-0.56b0-py3-none-any.whl.metadata (2.1 kB)
Collecting opentelemetry-sdk<2.0.0,>=1.30.0 (from strands-agents==1.0.1)
  Downloading opentelemetry_sdk-1.35.0-py3-none-any.whl.metadata (1.5 kB)
Requirement already satisfied: pydantic<3.0.0,>=2.0.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from strands-agents==1.0.1) (2.9.2)
Collecting typing-extensions<5.0.0,>=4.13.2 (from strands-agents==1.0.1)
  Downloading typing_extensions-4.14.1-py3-none-any.whl.metadata (3.0 kB)
Collecting watchdog<7.0.0,>=6.0.0 (from strands-agents==1.0.1)
  Downloading watchdog-6.0.0-cp310-cp310-macosx_11_0_arm64.whl.metadata (44 kB)
Collecting starlette>=0.46.2 (from bedrock-agentcore==0.1.0)
  Downloading starlette-0.47.2-py3-none-any.whl.metadata (6.2 kB)
Requirement already satisfied: urllib3>=1.26.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from bedrock-agentcore==0.1.0) (2.2.1)
Collecting uvicorn>=0.34.2 (from bedrock-agentcore==0.1.0)
  Downloading uvicorn-0.35.0-py3-none-any.whl.metadata (6.5 kB)
Collecting httpx>=0.28.1 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting jinja2>=3.1.6 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting prompt-toolkit>=3.0.51 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading prompt_toolkit-3.0.51-py3-none-any.whl.metadata (6.4 kB)
Collecting pyyaml>=6.0.2 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading PyYAML-6.0.2-cp310-cp310-macosx_11_0_arm64.whl.metadata (2.1 kB)
Requirement already satisfied: requests>=2.25.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from bedrock-agentcore-starter-toolkit==0.1.1) (2.32.3)
Collecting rich<15.0.0,>=14.0.0 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading rich-14.1.0-py3-none-any.whl.metadata (18 kB)
Collecting toml>=0.10.2 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading toml-0.10.2-py2.py3-none-any.whl.metadata (7.1 kB)
Collecting typer>=0.16.0 (from bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading typer-0.16.0-py3-none-any.whl.metadata (15 kB)
Collecting jmespath<2.0.0,>=0.7.1 (from boto3<2.0.0,>=1.26.0->strands-agents==1.0.1)
  Downloading jmespath-1.0.1-py3-none-any.whl.metadata (7.6 kB)
Collecting s3transfer<0.14.0,>=0.13.0 (from boto3<2.0.0,>=1.26.0->strands-agents==1.0.1)
  Downloading s3transfer-0.13.1-py3-none-any.whl.metadata (1.7 kB)
Requirement already satisfied: python-dateutil<3.0.0,>=2.1 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from botocore<2.0.0,>=1.29.0->strands-agents==1.0.1) (2.9.0.post0)
Requirement already satisfied: anyio>=4.5 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1) (4.6.2.post1)
Collecting httpx-sse>=0.4 (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading httpx_sse-0.4.1-py3-none-any.whl.metadata (9.4 kB)
Collecting jsonschema>=4.20.0 (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading jsonschema-4.25.0-py3-none-any.whl.metadata (7.7 kB)
Collecting pydantic-settings>=2.5.2 (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading pydantic_settings-2.10.1-py3-none-any.whl.metadata (3.4 kB)
Collecting python-multipart>=0.0.9 (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading python_multipart-0.0.20-py3-none-any.whl.metadata (1.8 kB)
Collecting sse-starlette>=1.6.1 (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading sse_starlette-3.0.0-py3-none-any.whl.metadata (11 kB)
Collecting importlib-metadata<8.8.0,>=6.0 (from opentelemetry-api<2.0.0,>=1.30.0->strands-agents==1.0.1)
  Downloading importlib_metadata-8.7.0-py3-none-any.whl.metadata (4.8 kB)
Collecting zipp>=3.20 (from importlib-metadata<8.8.0,>=6.0->opentelemetry-api<2.0.0,>=1.30.0->strands-agents==1.0.1)
  Downloading zipp-3.23.0-py3-none-any.whl.metadata (3.6 kB)
Collecting opentelemetry-instrumentation==0.56b0 (from opentelemetry-instrumentation-threading<1.00b0,>=0.51b0->strands-agents==1.0.1)
  Downloading opentelemetry_instrumentation-0.56b0-py3-none-any.whl.metadata (6.7 kB)
Requirement already satisfied: wrapt<2.0.0,>=1.0.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from opentelemetry-instrumentation-threading<1.00b0,>=0.51b0->strands-agents==1.0.1) (1.17.0)
Collecting opentelemetry-semantic-conventions==0.56b0 (from opentelemetry-instrumentation==0.56b0->opentelemetry-instrumentation-threading<1.00b0,>=0.51b0->strands-agents==1.0.1)
  Downloading opentelemetry_semantic_conventions-0.56b0-py3-none-any.whl.metadata (2.4 kB)
Requirement already satisfied: packaging>=18.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from opentelemetry-instrumentation==0.56b0->opentelemetry-instrumentation-threading<1.00b0,>=0.51b0->strands-agents==1.0.1) (24.0)
Requirement already satisfied: annotated-types>=0.6.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from pydantic<3.0.0,>=2.0.0->strands-agents==1.0.1) (0.7.0)
Requirement already satisfied: pydantic-core==2.23.4 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from pydantic<3.0.0,>=2.0.0->strands-agents==1.0.1) (2.23.4)
Requirement already satisfied: six>=1.5 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from python-dateutil<3.0.0,>=2.1->botocore<2.0.0,>=1.29.0->strands-agents==1.0.1) (1.16.0)
Collecting markdown-it-py>=2.2.0 (from rich<15.0.0,>=14.0.0->bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading markdown_it_py-3.0.0-py3-none-any.whl.metadata (6.9 kB)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from rich<15.0.0,>=14.0.0->bedrock-agentcore-starter-toolkit==0.1.1) (2.17.2)
Requirement already satisfied: idna>=2.8 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from anyio>=4.5->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1) (3.6)
Requirement already satisfied: sniffio>=1.1 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from anyio>=4.5->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1) (1.3.1)
Requirement already satisfied: exceptiongroup>=1.0.2 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from anyio>=4.5->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1) (1.2.2)
Requirement already satisfied: certifi in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from httpx>=0.28.1->bedrock-agentcore-starter-toolkit==0.1.1) (2024.2.2)
Requirement already satisfied: httpcore==1.* in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from httpx>=0.28.1->bedrock-agentcore-starter-toolkit==0.1.1) (1.0.7)
Requirement already satisfied: h11<0.15,>=0.13 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from httpcore==1.*->httpx>=0.28.1->bedrock-agentcore-starter-toolkit==0.1.1) (0.14.0)
Requirement already satisfied: MarkupSafe>=2.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from jinja2>=3.1.6->bedrock-agentcore-starter-toolkit==0.1.1) (2.1.5)
Requirement already satisfied: attrs>=22.2.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from jsonschema>=4.20.0->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1) (24.2.0)
Collecting jsonschema-specifications>=2023.03.6 (from jsonschema>=4.20.0->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading jsonschema_specifications-2025.4.1-py3-none-any.whl.metadata (2.9 kB)
Collecting referencing>=0.28.4 (from jsonschema>=4.20.0->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading referencing-0.36.2-py3-none-any.whl.metadata (2.8 kB)
Collecting rpds-py>=0.7.1 (from jsonschema>=4.20.0->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading rpds_py-0.26.0-cp310-cp310-macosx_11_0_arm64.whl.metadata (4.2 kB)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich<15.0.0,>=14.0.0->bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Collecting wcwidth (from prompt-toolkit>=3.0.51->bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading wcwidth-0.2.13-py2.py3-none-any.whl.metadata (14 kB)
Requirement already satisfied: python-dotenv>=0.21.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from pydantic-settings>=2.5.2->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1) (1.0.1)
Collecting typing-inspection>=0.4.0 (from pydantic-settings>=2.5.2->mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading typing_inspection-0.4.1-py3-none-any.whl.metadata (2.6 kB)
Requirement already satisfied: charset-normalizer<4,>=2 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from requests>=2.25.0->bedrock-agentcore-starter-toolkit==0.1.1) (3.3.2)
Collecting anyio>=4.5 (from mcp<2.0.0,>=1.8.0->strands-agents==1.0.1)
  Downloading anyio-4.9.0-py3-none-any.whl.metadata (4.7 kB)
Requirement already satisfied: click>=8.0.0 in /Users/uchinishi.koichi/.pyenv/versions/3.10.13/lib/python3.10/site-packages (from typer>=0.16.0->bedrock-agentcore-starter-toolkit==0.1.1) (8.1.7)
Collecting shellingham>=1.3.0 (from typer>=0.16.0->bedrock-agentcore-starter-toolkit==0.1.1)
  Downloading shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
Downloading strands_agents-1.0.1-py3-none-any.whl (162 kB)
Downloading bedrock_agentcore-0.1.0-py3-none-any.whl (48 kB)
Downloading bedrock_agentcore_starter_toolkit-0.1.1-py3-none-any.whl (77 kB)
Downloading boto3-1.39.14-py3-none-any.whl (139 kB)
Downloading botocore-1.39.14-py3-none-any.whl (13.9 MB)
   ━━━━━━━━━━ 13.9/13.9  24.7 MB/s eta 0:00:00
              MB
Downloading docstring_parser-0.17.0-py3-none-any.whl (36 kB)
Downloading jmespath-1.0.1-py3-none-any.whl (20 kB)
Downloading mcp-1.12.2-py3-none-any.whl (158 kB)
Downloading opentelemetry_api-1.35.0-py3-none-any.whl (65 kB)
Downloading importlib_metadata-8.7.0-py3-none-any.whl (27 kB)
Downloading opentelemetry_instrumentation_threading-0.56b0-py3-none-any.whl (9.3 kB)
Downloading opentelemetry_instrumentation-0.56b0-py3-none-any.whl (31 kB)
Downloading opentelemetry_semantic_conventions-0.56b0-py3-none-any.whl (201 kB)
Downloading opentelemetry_sdk-1.35.0-py3-none-any.whl (119 kB)
Downloading rich-14.1.0-py3-none-any.whl (243 kB)
Downloading s3transfer-0.13.1-py3-none-any.whl (85 kB)
Downloading typing_extensions-4.14.1-py3-none-any.whl (43 kB)
Downloading watchdog-6.0.0-cp310-cp310-macosx_11_0_arm64.whl (89 kB)
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
Downloading httpx_sse-0.4.1-py3-none-any.whl (8.1 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading jsonschema-4.25.0-py3-none-any.whl (89 kB)
Downloading jsonschema_specifications-2025.4.1-py3-none-any.whl (18 kB)
Downloading markdown_it_py-3.0.0-py3-none-any.whl (87 kB)
Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Downloading prompt_toolkit-3.0.51-py3-none-any.whl (387 kB)
Downloading pydantic_settings-2.10.1-py3-none-any.whl (45 kB)
Downloading python_multipart-0.0.20-py3-none-any.whl (24 kB)
Downloading PyYAML-6.0.2-cp310-cp310-macosx_11_0_arm64.whl (171 kB)
Downloading referencing-0.36.2-py3-none-any.whl (26 kB)
Downloading rpds_py-0.26.0-cp310-cp310-macosx_11_0_arm64.whl (357 kB)
Downloading sse_starlette-3.0.0-py3-none-any.whl (11 kB)
Downloading anyio-4.9.0-py3-none-any.whl (100 kB)
Downloading starlette-0.47.2-py3-none-any.whl (72 kB)
Downloading toml-0.10.2-py2.py3-none-any.whl (16 kB)
Downloading typer-0.16.0-py3-none-any.whl (46 kB)
Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Downloading typing_inspection-0.4.1-py3-none-any.whl (14 kB)
Downloading uvicorn-0.35.0-py3-none-any.whl (66 kB)
Downloading zipp-3.23.0-py3-none-any.whl (10 kB)
Downloading wcwidth-0.2.13-py2.py3-none-any.whl (34 kB)
Installing collected packages: wcwidth, zipp, watchdog, typing-extensions, toml, shellingham, rpds-py, pyyaml, python-multipart, prompt-toolkit, mdurl, jmespath, jinja2, httpx-sse, docstring-parser, uvicorn, typing-inspection, referencing, markdown-it-py, importlib-metadata, botocore, anyio, starlette, sse-starlette, s3transfer, rich, opentelemetry-api, jsonschema-specifications, httpx, typer, pydantic-settings, opentelemetry-semantic-conventions, jsonschema, boto3, opentelemetry-sdk, opentelemetry-instrumentation, mcp, bedrock-agentcore, opentelemetry-instrumentation-threading, bedrock-agentcore-starter-toolkit, strands-agents
  Attempting uninstall: watchdog
    Found existing installation: watchdog 4.0.0
    Uninstalling watchdog-4.0.0:
      Successfully uninstalled watchdog-4.0.0
  Attempting uninstall: typing-extensions
    Found existing installation: typing_extensions 4.12.2
    Uninstalling typing_extensions-4.12.2:
      Successfully uninstalled typing_extensions-4.12.2
  Attempting uninstall: pyyaml
    Found existing installation: PyYAML 6.0.1
    Uninstalling PyYAML-6.0.1:
      Successfully uninstalled PyYAML-6.0.1
  Attempting uninstall: jinja2
    Found existing installation: Jinja2 3.1.3
    Uninstalling Jinja2-3.1.3:
      Successfully uninstalled Jinja2-3.1.3
  Attempting uninstall: anyio
    Found existing installation: anyio 4.6.2.post1
    Uninstalling anyio-4.6.2.post1:
      Successfully uninstalled anyio-4.6.2.post1
  Attempting uninstall: httpx
    Found existing installation: httpx 0.27.2
    Uninstalling httpx-0.27.2:
      Successfully uninstalled httpx-0.27.2
Successfully installed anyio-4.9.0 bedrock-agentcore-0.1.0 bedrock-agentcore-starter-toolkit-0.1.1 boto3-1.39.14 botocore-1.39.14 docstring-parser-0.17.0 httpx-0.28.1 httpx-sse-0.4.1 importlib-metadata-8.7.0 jinja2-3.1.6 jmespath-1.0.1 jsonschema-4.25.0 jsonschema-specifications-2025.4.1 markdown-it-py-3.0.0 mcp-1.12.2 mdurl-0.1.2 opentelemetry-api-1.35.0 opentelemetry-instrumentation-0.56b0 opentelemetry-instrumentation-threading-0.56b0 opentelemetry-sdk-1.35.0 opentelemetry-semantic-conventions-0.56b0 prompt-toolkit-3.0.51 pydantic-settings-2.10.1 python-multipart-0.0.20 pyyaml-6.0.2 referencing-0.36.2 rich-14.1.0 rpds-py-0.26.0 s3transfer-0.13.1 shellingham-1.5.4 sse-starlette-3.0.0 starlette-0.47.2 strands-agents-1.0.1 toml-0.10.2 typer-0.16.0 typing-extensions-4.14.1 typing-inspection-0.4.1 uvicorn-0.35.0 watchdog-6.0.0 wcwidth-0.2.13 zipp-3.23.0
Usage: agentcore [OPTIONS] COMMAND [ARGS]...
Try 'agentcore --help' for help.
╭─ Error ────────────────────────────────────╮
│ No such option: --version                  │
╰────────────────────────────────────────────╯
