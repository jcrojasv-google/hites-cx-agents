def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """Executes *before* the agent begins its main processing logic.
    Return a 'Content' object instead of 'None' to skip execution (LLM/tools)
    and immediately return this object as the final answer.
    This is useful for intercepting a request, enforcing access control, or
    handling a simple query directly without engaging the full agent.
    """
    print(callback_context.session_id)
    if callback_context.state.get("session_id", "") == "":
        # Fix: Store the session_id string, not the whole context object
        callback_context.state["session_id"] = callback_context.session_id
    return None