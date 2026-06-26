# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import cached_property
import os

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import Client
from google.genai import types
import google.auth

from app.tools import redeem_discount_code

try:
    _, project_id = google.auth.default()
except Exception:
    project_id = "mock-project-id"

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id or "mock-project-id"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


class CustomGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyD-mock-key-value-12345"
        return Client(api_key=api_key)

    @cached_property
    def _live_api_client(self) -> Client:
        api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyD-mock-key-value-12345"
        return Client(api_key=api_key)


root_agent = Agent(
    name="retail_shopping_assistant",
    model=CustomGemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an AI shopping assistant for a retail store. "
        "Help customers find products, answer questions, and redeem discount codes. "
        "When a customer wants to redeem a discount code, you must ask for both their registered user ID and the code, "
        "and then call the redeem_discount_code tool to process it."
    ),
    tools=[redeem_discount_code],
)

app = App(
    root_agent=root_agent,
    name="app",
)
