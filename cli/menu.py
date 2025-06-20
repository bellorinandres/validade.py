#!/data/data/com.termux/files/usr/bin/python3
import json
import os
from conn import (
    agregar_validade,
    listar_validades_desde_hoy,
    buscar_validade_por_codigo,
    obtener_top_6,
    limpiar_registros_vencidos,
    cerrar_conexion,
)


# 📦 Cargar configuración
def cargar_configuracion():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        config = {"idioma": "es", "limpieza_automatica_dias": 15}
        guardar_configuracion(config)
        return config


# 💾 Guardar configuración
def guardar_configuracion(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


# 🌍 Cargar idioma
def cargar_idioma(idioma):
    try:
        with open(f"{idioma}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Archivo de idioma {idioma}.json no encontrado")
        exit(1)


# 📲 Compartir por WhatsApp
def compartir_por_whatsapp(mensaje):
    mensaje_formateado = mensaje.replace(" ", "%20").replace("\n", "%0A")
    url = f"https://wa.me/?text={mensaje_formateado}"
    os.system(f"termux-open-url '{url}'")


# 🔧 Menú de configuración
def configuracion():
    global datos  # para modificar la variable global

    while True:
        print("\n===== CONFIGURACIÓN =====")
        print("1. Cambiar idioma (es/pt)")
        print("2. Configurar limpieza automática")
        print("3. Volver")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            idioma = input("Idioma (es/pt): ").lower()
            if idioma in ["es", "pt"]:
                config["idioma"] = idioma
                guardar_configuracion(config)
                datos = cargar_idioma(idioma)  # recargar idioma al vuelo
                print("✅ Idioma actualizado.")
            else:
                print("❌ Idioma no válido.")

        elif opcion == "2":
            # ... resto igual ...
            pass

        elif opcion == "3":
            return

        else:
            print("❌ Opción inválida.")


# 🚀 Función principal
def main():
    limpiar_registros_vencidos(config.get("limpieza_automatica_dias", 0))

    print("\n" + "=" * 40)
    print(datos["titulo"])
    print("=" * 40)

    top = obtener_top_6()
    if top:
        print(datos["mensajes"]["top_productos"])
        for t in top:
            print(f"🆔 Código: {t[0]} | Validade: {t[1]} | Cantidad: {t[2]}")
    else:
        print(datos["mensajes"]["sin_registros"])

    while True:
        try:
            print("\n" + "=" * 40)
            print(datos["opciones_menu"]["agregar"])
            print(datos["opciones_menu"]["listar"])
            print(datos["opciones_menu"]["buscar"])
            print(datos["opciones_menu"]["config"])
            print(datos["opciones_menu"]["salir"])

            opcion = input(datos["mensajes"]["seleccion"])

            if opcion == "1":
                codigo = int(input(datos["mensajes"]["ingresa_codigo"]))
                validade = input(datos["mensajes"]["ingresa_validade"])
                cantidad = int(input(datos["mensajes"]["ingresa_cantidad"]))
                try:
                    agregar_validade(codigo, validade, cantidad)
                    print(datos["mensajes"]["agregado_exito"])
                except Exception as e:
                    print(datos["mensajes"]["registro_duplicado"])

            elif opcion == "2":
                registros = listar_validades_desde_hoy()
                if registros:
                    mensaje = "ID | Código | Validade | Cantidad\n"
                    mensaje += "-" * 40 + "\n"
                    for r in registros:
                        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
                        mensaje += f"{r[0]} | {r[1]} | {r[2]} | {r[3]}\n"
                    compartir = input("¿Compartir por WhatsApp? (s/n): ").lower()
                    if compartir == "s":
                        compartir_por_whatsapp(mensaje)
                else:
                    print(datos["mensajes"]["sin_registros"])

            elif opcion == "3":
                codigo = int(input(datos["mensajes"]["ingresa_codigo_buscar"]))
                registros = buscar_validade_por_codigo(codigo)
                if registros:
                    mensaje = "ID | Código | Validade | Cantidad\n"
                    mensaje += "-" * 40 + "\n"
                    for r in registros:
                        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
                        mensaje += f"{r[0]} | {r[1]} | {r[2]} | {r[3]}\n"
                    compartir = input("¿Compartir por WhatsApp? (s/n): ").lower()
                    if compartir == "s":
                        compartir_por_whatsapp(mensaje)
                else:
                    print(datos["mensajes"]["sin_registros"])

            elif opcion == "4":
                configuracion()

            elif opcion == "5":
                print(datos["mensajes"]["despedida"])
                cerrar_conexion()
                break

            else:
                print(datos["mensajes"]["opcion_invalida"])

            input("\n" + datos["mensajes"]["continuar"])

        except KeyboardInterrupt:
            print("\n" + datos["mensajes"]["cancelado"])
            cerrar_conexion()
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\n" + datos["mensajes"]["continuar"])


# Inicializar
config = cargar_configuracion()
datos = cargar_idioma(config.get("idioma", "es"))

if __name__ == "__main__":
    main()
