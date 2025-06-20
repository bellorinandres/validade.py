import * as SQLite from "expo-sqlite";

let db: SQLite.SQLiteDatabase;

// Inicializar base de datos
export const initDatabase = async () => {
  db = await SQLite.openDatabaseAsync("validades.db");

  await db.execAsync(`
    PRAGMA journal_mode = WAL;
    CREATE TABLE IF NOT EXISTS validades (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      codigo INTEGER NOT NULL,
      validade TEXT NOT NULL,
      cantidad INTEGER NOT NULL
    );
  `);
};

// Agregar validade con verificación de duplicados
export const agregarValidade = async (
  codigo: number,
  validade: string,
  cantidad: number
) => {
  const existe = await db.getFirstAsync(
    "SELECT * FROM validades WHERE codigo = ? AND validade = ?",
    [codigo, validade]
  );

  if (existe) {
    throw new Error("❌ Ya existe ese código con esa validade.");
  }

  const result = await db.runAsync(
    "INSERT INTO validades (codigo, validade, cantidad) VALUES (?, ?, ?)",
    codigo,
    validade,
    cantidad
  );

  return result.lastInsertRowId;
};

// Listar validades vigentes (solo desde hoy en adelante)
export const listarValidades = async () => {
  const rows = await db.getAllAsync(
    `SELECT * FROM validades 
     WHERE validade >= DATE('now') 
     ORDER BY validade ASC`
  );
  return rows;
};

// Buscar por código (solo válidos desde hoy)
export const buscarPorCodigo = async (codigo: number) => {
  const rows = await db.getAllAsync(
    `SELECT * FROM validades 
     WHERE codigo = ? 
     AND validade >= DATE('now') 
     ORDER BY validade ASC`,
    [codigo]
  );
  return rows;
};

// Obtener TOP 6 productos con mayor cantidad, ordenados por validade más próxima
export const obtenerTop6 = async () => {
  const rows = await db.getAllAsync(
    `SELECT codigo, validade, SUM(cantidad) as total 
     FROM validades 
     WHERE validade >= DATE('now') 
     GROUP BY codigo, validade 
     ORDER BY total DESC, validade ASC 
     LIMIT 6`
  );
  return rows;
};

// Limpiar registros vencidos (anteriores a hoy menos X días)
export const limpiarRegistrosVencidos = async (dias: number) => {
  if (dias <= 0) return;

  const result = await db.runAsync(
    `DELETE FROM validades 
     WHERE validade < DATE('now', '-${dias} days')`
  );

  return result.changes;
};
