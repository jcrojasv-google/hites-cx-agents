from typing import Optional

def after_agent_callback(callback_context: CallbackContext) -> Optional[Content]:
  """
  Executes after the agent finishes, but before the result is returned to the user.

  Return 'None' to allow the agent's default behavior to proceed.
  The 'Content' object that the agent generated will be returned
  to the user without modification.

  This is a perfect spot for logging the final response or performing cleanup
  actions without altering the outcome.
  """
  # Log the agent's output
  print(callback_context.get_last_agent_output())
  # Returning None allows the agent's generated result to pass through.
  return None