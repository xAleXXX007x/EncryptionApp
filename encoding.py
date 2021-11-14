import bitarray
from bitstring import BitArray

# Перевод байтов в двоичную запись
def bitEncode(bytes):
  ba = bitarray.bitarray()
  ba.frombytes(bytes)
  return ba.to01()

# Перевод двоичной записи в байты
def bitDecode(bitcode):
  b = BitArray(bin=bitcode)
  return b.bytes

# Вспомогательная функция перестановки блока бит по заданной таблице
def toPattern(block, pattern):
  output = ""

  for i in pattern:
    output += block[i - 1]
  
  return output

# Разбиение множества бит на блоки по 64
def toBlocks(bitcode):
  output = []
  mod = len(bitcode) % 64

  # Если последний блок имеет недостаточную длину, то он дополняется нулевыми битами
  if (mod != 0):
    for i in range(0, int(mod / 8)):
      bitcode += "00000000"

  while (len(bitcode) >= 64):
    block = bitcode[:64]
    output.append(block)
    bitcode = bitcode[64:]

  return output

# Соединение блоков бит в единое множество
def bitcodeFromBlocks(blocks):
  output = ""

  for block in blocks:
    output += block

  # Удаление нулевых бит, добавленных ранее
  while (output.endswith("00000000")):
    output = output[:-8]
  
  return output

# Функция начальной перестановки битов
def initialPermutation(block):
  return toPattern(block, [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
  ])

# Функция обратной перестановки битов
def endingPermutation(block):
  return toPattern(block, [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9,  49, 17, 57, 25
  ])

# Функция расширения блока в 32 бит до 48
def E(block):
  return toPattern(block, [
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
  ])

# Преобразование строкового ключа в набор из 16 битовых ключей
def generateKeys(key):
  if (len(key) != 7):
    raise Exception("Key length must be exactly 7 characters")

  bitcode = bitEncode(key.encode("utf-8"))
  key64 = ""

  # Дополнение ключа битами так, чтобы каждый байт содержал
  # нечетное количество единиц
  for i in range(0, 7):
    byte = bitcode[i * 8:(i + 1) * 8]

    if (byte.count("1") % 2 == 0):
      byte += "1"
    else:
      byte += "0"
    
    key64 += byte
  
  # Перестановка расширенного ключа
  key56 = toPattern(key64, [
    57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4
  ])

  keys = []

  # Проведение левого циклического сдвига по заданной таблице
  C, D = key56[:28], key56[28:]

  shiftOffset = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

  for i in range(0, 16):
    offset = shiftOffset[i]
    C, D = leftShift(C, offset), leftShift(D, offset)
    keys.append([C, D])
  
  # Конечная перестановка ключей
  pattern = [
    14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10, 23, 19, 12, 4,
    26, 8,  16, 7,  27, 20, 13, 2,  41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
  ]

  output = []

  for keyPair in keys:
    key56 = keyPair[0] + keyPair[1]
    output.append(toPattern(key56, pattern))

  return output

# Вспомогательная функция проведения левого циклического сдвига
def leftShift(key, offset):
  chars = key[:offset]
  return key[offset:] + chars

# Проведение операции XOR (Исключающего ИЛИ) для двух блоков бит
def xor(a, b):
  if (len(a) != len(b)):
    raise Exception("A length not equal to B length")

  output = ""

  for i in range(0, len(a)):
    if (a[i] != b[i]):
      output += "1"
    else:
      output += "0"
  
  return output

# Функция F, использующаяся в раунде сети Фейстеля
def F(block, key):
  bitcode = E(block)
  bitcode = xor(bitcode, key)

  bits = ""

  for i in range(0, 8):
    bits += S(i, bitcode[i * 6:i * 6 + 6])

  return toPattern(bits, [
    16, 7,  20, 21, 29, 12, 28, 17,
    1,  15, 23, 26, 5,  18, 31, 10,
    2,  8,  24, 14, 32, 27, 3,  9,
    19, 13, 30, 6,  22, 11, 4,  25
  ])

# Функции преобразования для S-box'ов
SPatterns = [
  [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
  ],
  [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
  ],
  [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
  ],
  [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
  ],
  [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
  ],
  [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
  ],
  [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
  ],
  [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
  ]
]

# Функции преобразования S-box
def S(i, block):
  pattern = SPatterns[i]

  # Первый и последний разряды составляют номер строки (0-3)
  row = int(block[0] + block[5], 2)
  # Остальные разряды - номер столбца (0-15)
  column = int(block[1:5], 2)

  # Полученное число преобразуется в двоичное
  return "{0:04b}".format(pattern[row][column])

# Функция Фейстеля
def feistel(block, keys):
  # Проведение начальной перестановки блока
  block = initialPermutation(block)

  output = ""

  L, R = block[:32], block[32:]

  # Проведение 16 раундов функции Фейстеля
  for i in range(0, 16):
    L = xor(L, F(R, keys[i]))
    L, R = R, L

  output = L + R

  # Проведение конечной (обратной) перестановки блока
  return endingPermutation(output)

# Обратная функция Фейстеля
def fromFeistel(block, keys):
  # Проведение начальной перестановки блока
  block = initialPermutation(block)

  output = ""

  L, R = block[:32], block[32:]

  # Проведение 16 раундов обратной функции Фейстеля
  for i in range(15, -1, -1):
    L, R = R, L
    L = xor(L, F(R, keys[i]))
  
  output = L + R

  # Проведение конечной (обратной) перестановки блока
  return endingPermutation(output)

# Шифрование вектора инициализации из строки
def generateIv(iv, keys):
  return feistel(toBlocks(bitEncode(iv.encode("utf-8")))[0], keys)

# Основная функция шифрования DES-OFB
def encodeDES(bytes, key, iv):
  encoded = bitEncode(bytes)
  blocks = toBlocks(encoded)
  keys = generateKeys(key)
  prevIv = generateIv(iv, keys)

  encodedBlocks = []
  
  # Режим шифрования OFB
  # Шифруется не сам блок, а инициализирующий вектор, причем многократно
  # Полученное значение суммируется по модулю 2 с исходным блоком бит
  for block in blocks:
    encodedBlocks.append(xor(block, prevIv))
    prevIv = feistel(prevIv, keys)
  
  # Полученное значение возвращается в виде множества байт
  return bitDecode(''.join(encodedBlocks))

# Основная функция расшифровки DES-OFB
def decodeDES(bytes, key, iv):
  bitcode = bitEncode(bytes)
  keys = generateKeys(key)
  blocks = toBlocks(bitcode)
  prevIv = generateIv(iv, keys)

  decodedBlocks = []

  for block in blocks:
    decodedBlocks.append(xor(block, prevIv))
    prevIv = feistel(prevIv, keys)

  bitcode = bitcodeFromBlocks(decodedBlocks)

  return bitDecode(bitcode)
