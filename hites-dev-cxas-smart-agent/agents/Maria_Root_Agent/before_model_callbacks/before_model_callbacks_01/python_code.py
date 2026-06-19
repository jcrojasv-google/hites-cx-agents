import json
import base64
from typing import Optional, Any

def get_payload_part(payload_string: str):
    return Part(inline_data=ces_internal.Blob(data=base64.b64encode(payload_string.encode("utf-8")), mime_type="application/json"))

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # ── Intercepción de transfer_agent para evitar latencia del LLM en Turno 2 ──
    try:
        for event in reversed(callback_context.events):
            if event.is_user():
                break
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_response and part.function_response.name == "transfer_agent":
                      telephony_payload = callback_context.variables.get("TELEPHONY_PAYLOAD", {})
                      end_session_args = {
                          "session_escalated": True,
                          "params": {
                              "TELEPHONY_PAYLOAD": telephony_payload
                          }
                      }
                      return LlmResponse.from_parts([
                          Part.from_function_call(name="end_session", args=end_session_args)
                      ])
    except Exception as e:
        print(f"Error in transfer_agent interception in before_model_callback: {e}")

    # ── Lógica original de ending_session ────────────────────────────────────
    ending_session = callback_context.variables.get("ending_session", "")
    if ending_session:
        print("ending session")
        payload = {"ujet": {"type": "action", "action": "end"}}
        callback_context.set_variable("TELEPHONY_PAYLOAD", payload)

    return None