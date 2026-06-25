import os
from langchain_community.llms import Ollama
# 🌟 [수정] TextLoader 대신 PDF용 Loader를 가져옵니다.
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ==========================================
# 1. Ollama 컨테이너 연동 (두뇌: EXAONE)
# ==========================================
llm = Ollama(
    base_url="http://127.0.0.1:11434", 
    model="exaone3.5:2.4b"
)

# ==========================================
# 2. RAG 구현 (PDF 로드 -> 청킹 -> Vector DB 저장)
# ==========================================
print("📂 [RAG] 보안 규정 PDF 문서를 읽어오는 중...")

# 🌟 [수정] 바탕화면 security-chatbot/data/ 폴더 안에 있는 PDF 파일 경로를 지정합니다.
# 파일명이 정확히 일치해야 합니다. (예: 사내_정보보안_규정.pdf)
pdf_path = "data/security_rule.pdf" 
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# 보안 규정은 조항 단위 문맥이 중요하므로 500자 단위로 쪼갬
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

print(f"🧩 [RAG] PDF 문서를 {len(docs)}개의 조각으로 분할 완료.")

# M1 Mac에서 가볍고 완벽하게 작동하는 한국어 오픈소스 임베딩 모델
print("🤖 [RAG] 로컬 임베딩 모델 로드 중 (최초 1회 다운로드)...")
embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")

# 메모리 기반 가벼운 로컬 Vector DB 구축
print("💾 [RAG] Vector DB(Chroma) 구축 및 데이터 인덱싱 중...")
vector_db = Chroma.from_documents(docs, embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

print("✅ RAG 파이프라인 준비 완료!\n" + "="*50)

# ==========================================
# 3. 상시 가이드라인(Harness) 주입 및 추론 함수
# ==========================================
def ask_security_chatbot(user_question):
    # [RAG] 사용자의 질문과 가장 관련된 규정 본문 검색
    relevant_docs = retriever.invoke(user_question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # [Harness] AI가 절대로 벗어나지 못하게 제약 조건을 거는 시스템 프롬프트(가이드라인)
    system_guideline = f"""
[상시 가이드라인 (System Harness)]
당신은 회사의 '사내 정보보안 규정'을 안내하는 전문 보안 Agent입니다. 
다음 지침을 반드시 철저하게 준수하여 답변하세요.

1. 반드시 아래 제공된 [보안 규정 컨텍스트]의 내용에만 기반하여 답변하세요.
2. 규정에 나와 있지 않은 내용은 절대로 임의로 추측하거나 지어내어 답변하지 마세요 (할루시네이션 절대 금지).
3. 만약 제공된 컨텍스트에서 질문에 대한 답을 찾을 수 없다면, 솔직하게 "해당 내용은 현재 사내 정보보안 규정에서 확인할 수 없습니다. 보안운영팀에 추가 문의하시기 바랍니다."라고 답변하세요.
4. 답변은 친절하되 단호하고 명확한 어조로 작성하세요.

[보안 규정 컨텍스트]
{context}
"""

    # 가이드라인(프롬프트)과 사용자의 질문을 결합하여 EXAONE에게 전달
    full_prompt = f"{system_guideline}\n\n사용자 질문: {user_question}\n답변:"
    
    # LLM 실행
    response = llm.invoke(full_prompt)
    return response

# ==========================================
# 4. 챗봇 상시 작동 테스트
# ==========================================
if __name__ == "__main__":
    print("🤖 정보보안 카테고리 챗봇이 활성화되었습니다.")
    print("정지하려면 '종료'를 입력하세요.\n")
    
    while True:
        query = input("질문 입력: ")
        if query.strip() == "종료":
            break
        
        if not query.strip():
            continue
            
        print("\n🔍 규정 검색 및 답변 생성 중...")
        answer = ask_security_chatbot(query)
        print(f"\n[챗봇 답변]:\n{answer}")
        print("\n" + "-"*50)