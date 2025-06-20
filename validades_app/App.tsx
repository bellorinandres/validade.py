import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  Button,
  TextInput,
  FlatList,
  StyleSheet,
  Alert,
  Pressable,
  Platform,
} from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";

import { initDatabase, agregarValidade, listarValidades } from "./database"; // Ajusta la ruta según tu proyecto

export default function AgregarValidade() {
  const [codigo, setCodigo] = useState("");
  const [validade, setValidade] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [lista, setLista] = useState<any[]>([]);

  const [showPicker, setShowPicker] = useState(false);
  const [date, setDate] = useState(new Date());

  useEffect(() => {
    (async () => {
      await initDatabase();
      await cargarLista();
    })();
  }, []);

  const cargarLista = async () => {
    const datos = await listarValidades();
    setLista(datos);
  };

  const onChangeDate = (event: any, selectedDate?: Date) => {
    setShowPicker(Platform.OS === "ios"); // En iOS se mantiene abierto
    if (selectedDate) {
      setDate(selectedDate);
      const isoDate = selectedDate.toISOString().split("T")[0]; // YYYY-MM-DD
      setValidade(isoDate);
    }
  };

  const agregar = async () => {
    if (!codigo || !validade || !cantidad) {
      Alert.alert("❌ Campos vacíos");
      return;
    }
    try {
      await agregarValidade(parseInt(codigo), validade, parseInt(cantidad));
      Alert.alert("✅ Agregado correctamente");
      setCodigo("");
      setValidade("");
      setCantidad("");
      setDate(new Date());
      await cargarLista();
    } catch (error: any) {
      Alert.alert(error.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Agregar Validade</Text>

      <TextInput
        placeholder="Código"
        keyboardType="numeric"
        value={codigo}
        onChangeText={setCodigo}
        style={styles.input}
      />

      <Pressable onPress={() => setShowPicker(true)}>
        <TextInput
          placeholder="Validade (YYYY-MM-DD)"
          value={validade}
          editable={false}
          style={[styles.input, { backgroundColor: "#f0f0f0" }]}
        />
      </Pressable>

      {showPicker && (
        <DateTimePicker
          value={date}
          mode="date"
          display="default"
          onChange={onChangeDate}
        />
      )}

      <TextInput
        placeholder="Cantidad"
        keyboardType="numeric"
        value={cantidad}
        onChangeText={setCantidad}
        style={styles.input}
      />

      <Button title="Agregar" onPress={agregar} />

      <Text style={styles.subtitle}>Listado vigente:</Text>
      <FlatList
        data={lista}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>
            🆔 {item.codigo} | 📅 {item.validade} | 🔢 {item.cantidad}
          </Text>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
  subtitle: { marginTop: 20, fontWeight: "bold", fontSize: 18 },
  input: {
    borderWidth: 1,
    padding: 10,
    marginVertical: 5,
    borderRadius: 5,
  },
  item: {
    paddingVertical: 5,
  },
});
