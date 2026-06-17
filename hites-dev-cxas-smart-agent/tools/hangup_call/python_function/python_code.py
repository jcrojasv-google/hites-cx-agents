def hangup_call() -> dict:
    """
    Returns UJET hangup payload to be sent BEFORE end_session.
    Must be called as the very first action after farewell message.
    """
    return {
        "custom_payload": {
            "ujet": {
                "type": "action",
                "action": "end"
            }
        }
    }