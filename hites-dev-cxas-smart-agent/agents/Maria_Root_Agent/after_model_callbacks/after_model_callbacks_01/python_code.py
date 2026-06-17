from typing import Optional

def after_model_callback(
    callback_context: CallbackContext,
    llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Callback que se ejecuta despues de la respuesta del LLM.
    Devuelve None para indicar que no hay modificaciones.
    """
    return None
