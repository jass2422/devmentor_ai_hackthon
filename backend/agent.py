import asyncio
import os
from dotenv import load_dotenv
from vision_agents.core import Agent, User
from vision_agents.plugins.gemini import Realtime as GeminiRealtime
from vision_agents.plugins.getstream import Edge as GetStreamEdge
from google.genai.types import LiveConnectConfigDict, Modality, SpeechConfigDict

load_dotenv()

AGENT_ID = "devmentor-ai"

async def main():
    print("DevMentor AI starting...")

    edge = GetStreamEdge(
        api_key=os.getenv("STREAM_API_KEY"),
        api_secret=os.getenv("STREAM_API_SECRET"),
    )

    agent_user = User(
        id=AGENT_ID,
        name="DevMentor AI",
    )

    await edge.create_user(agent_user)
    print("Agent user ready!")

    # Gemini Live config with AUDIO response
    gemini_config = LiveConnectConfigDict(
        response_modalities=[Modality.AUDIO],
        speech_config=SpeechConfigDict(
            language_code="en-US",
        ),
    )

    agent = Agent(
        edge=edge,
        agent_user=agent_user,
        instructions="""
        You are DevMentor AI - a friendly, patient, and encouraging
        real-time coding mentor for beginner developers.

        IMPORTANT: You must respond with VOICE/AUDIO to every message.
        Keep responses short, clear and encouraging.

        Your personality:
        - Talk like a helpful senior developer friend
        - Never make the learner feel stupid
        - Celebrate small wins enthusiastically
        - Give short clear explanations
        - Always suggest what to try NEXT

        When someone asks a coding question:
        - Answer clearly and simply out loud
        - Give a short code example if needed
        - Ask does that make sense after explanations

        Start by saying: "Hey! I'm DevMentor AI. What coding question can I help you with today?"
        """,
        llm=GeminiRealtime(
            api_key=os.getenv("GEMINI_API_KEY"),
            config=gemini_config,
        ),
    )

    call = await agent.create_call(
        call_type="default",
        call_id="devmentor-session",
    )
    print("Call created!")

    async with agent.join(call):
        print("DevMentor AI is LIVE and listening!")
        print("Speak into your microphone — AI will respond with voice!")
        print("Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("DevMentor AI stopped.")