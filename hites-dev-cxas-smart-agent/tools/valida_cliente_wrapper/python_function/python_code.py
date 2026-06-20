import json
import re

def get_response_data(resp) -> dict:
    """
    Extrae el diccionario de datos de un objeto de respuesta de forma robusta.
    Soporta diccionarios nativos, métodos .json() y múltiples atributos del SDK de Google.
    """
    if isinstance(resp, dict):
        return resp
    if resp is None:
        return {}
        
    # 1. Probar método nativo .json() (estándar en wrappers de respuesta)
    if hasattr(resp, "json") and callable(resp.json):
        try:
            return resp.json()
        except:
            pass
            
    # 2. Probar atributos de des-serialización comunes
    for attr in ["response", "output", "content", "data"]:
        val = getattr(resp, attr, None)
        if val is not None:
            if isinstance(val, dict):
                return val
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except:
                    pass
    return {}

def valida_cliente_wrapper(rut: str = "") -> dict:
    """
    Valida el RUT y verifica si es cliente de Hites de forma consolidada.
    Retorna un diccionario estructurado con el resultado y actualiza el estado.
    """
    # 1. Obtener y limpiar el RUT (prioridad argumento, fallback al estado)
    rut_source = rut or context.state.get("rut", "")
    cleaned_rut = re.sub(r'[\.\-\s]', '', str(rut_source)).upper()
    
    if not cleaned_rut:
        print("[valida_cliente_wrapper] Error: No se proporcionó el RUT.")
        context.state["rut_valido"] = "false"
        context.state["es_cliente_hites"] = "false"
        return {"rut_valido": False, "es_cliente_hites": False}

    # 2. Validar RUT llamando a la tool nativa
    try:
        resp_rut = get_response_data(tools.valida_rut_validarRut({"rut": cleaned_rut}))
        params_rut = resp_rut.get("session_info", {}).get("parameters", {})
        rut_valido = params_rut.get("rut_valido", False)
    except Exception as e:
        print(f"[valida_cliente_wrapper] Error en validarRut: {e}")
        context.state["rut_valido"] = "false"
        context.state["es_cliente_hites"] = "false"
        return {"rut_valido": False, "es_cliente_hites": False}

    # 3. Si el RUT es válido, verificar si es Cliente Hites
    es_cliente = False
    nombre_cliente = ""
    nombre_completo = ""
    codigo_cliente = ""
    
    if rut_valido:
        try:
            resp_cliente = get_response_data(tools.valida_cliente_hites_validarCliente({"rut": cleaned_rut}))
            params_cliente = resp_cliente.get("session_info", {}).get("parameters", {})
            es_cliente = params_cliente.get("es_cliente_hites", False) or params_cliente.get("esClienteHites", False)
            nombre_cliente = params_cliente.get("nombreCliente", "")
            nombre_completo = params_cliente.get("nombreCompletoCliente", "")
            codigo_cliente = params_cliente.get("codigoCliente", "")
        except Exception as e:
            print(f"[valida_cliente_wrapper] Error en validarCliente: {e}")

    # 4. Calcular intentos fallidos
    intentos = 0 if rut_valido else int(context.state.get("intentos_fallidos") or 0) + 1

    # 5. Persistir todos los resultados consolidados en el estado de la sesión (snake_case)
    context.state["rut"] = cleaned_rut
    context.state["rut_valido"] = "true" if rut_valido else "false"
    context.state["es_cliente_hites"] = "true" if es_cliente else "false"
    context.state["intentos_fallidos"] = str(intentos)
    
    # Manejar asignación inteligente de nombre_cliente (primer nombre)
    if nombre_cliente:
        context.state["nombre_cliente"] = nombre_cliente
    elif nombre_completo:
        context.state["nombre_cliente"] = nombre_completo.split()[0]
        
    if nombre_completo:
        context.state["nombre_completo_cliente"] = nombre_completo
    if codigo_cliente:
        context.state["codigo_cliente"] = codigo_cliente

    # 6. Retornar el resultado estructurado
    response_data = {
        "rut": cleaned_rut,
        "rut_valido": rut_valido,
        "intentos_fallidos": intentos,
        "es_cliente_hites": es_cliente,
        "nombre_cliente": context.state.get("nombre_cliente", ""),
        "nombre_completo_cliente": context.state.get("nombre_completo_cliente", "")
    }
    
    print(f"[valida_cliente_wrapper Success] {response_data}")
    return response_data
