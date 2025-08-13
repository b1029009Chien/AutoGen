import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.ui import Console

async def main():
    # create ollama client
    ollama_client = OllamaChatCompletionClient(
        model="qwen:1.8b",
        base_url="http://localhost:11434",
        temperature=0.2
    )

    # Three Agent
    summarizer = AssistantAgent(
        name="summarizer",
        model_client=ollama_client,
        system_message="You are an expert at understanding course content, merging the transcript with the course outline into a concise and complete summary."
    )

    keypoint_extractor = AssistantAgent(
        name="keypoint_extractor",
        model_client=ollama_client,
        system_message="You are a keyword extraction expert, pull 5–15 keywords from a bullet-point list."
    )

    keyword_extractor = AssistantAgent(
        name="generate_questions",
        model_client=ollama_client,
        system_message="You are a question generation expert skilled at creating targeted course questions based on self-organized notes and distilled key points. Capable of transforming learning content and teaching materials into thought-provoking questions that promote critical thinking and deepen understanding."
    )

    # NOTE: you can skip input by pressing Enter.
    user_proxy = UserProxyAgent("user_proxy")

    # The outter-loop termination condition that will terminate the team when the user types "exit".
    termination = TextMentionTermination("exit", sources=["user_proxy"])

    team = RoundRobinGroupChat(
        [summarizer, keypoint_extractor, keyword_extractor, user_proxy],
        termination_condition=termination
    )
    
    # ---------- Data ----------
    course_transcript = """
    今天我們討論了人工智慧的歷史，從早期的符號推理到機器學習的崛起，
    以及深度學習的突破。我們講解了神經網路的基本結構與反向傳播，
    並用圖像分類作為例子介紹卷積神經網路。最後探討 AI 在語言處理、
    影像辨識、醫療診斷等領域的應用與挑戰。
    """

    course_outline = """
    1. 人工智慧歷史發展
    2. 機器學習與深度學習
    3. 神經網路結構與反向傳播
    4. 圖像分類與卷積神經網路
    5. AI 應用與挑戰
    """

    # input
    initial_prompt = f"""
        請根據以下逐字稿與課程大綱完成三階段整理：
        1. understanding course content
        2. Fing the keypoints
        3. Generated Question

        逐字稿：
        {course_transcript}

        課程大綱：
        {course_outline}
        """

    # === 開始對話並串流輸出 ===
    await Console(team.run_stream(task=initial_prompt))

    # 關閉 Ollama 客戶端
    await ollama_client.close()

if __name__ == "__main__":
    asyncio.run(main())