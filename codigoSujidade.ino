// Pinos
const int ledPin = 9;          // Pino onde o LED está ligado
const int ldrPin = A0;         // Pino analógico onde o LDR está ligado

// Variáveis para calibração
int valorLimpo = 217;          // Valor típico do LDR quando o LED está limpo
int valorSujo = 100;           // Valor típico do LDR quando o LED está muito sujo

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  delay(2000); // Aguarda inicialização
  digitalWrite(ledPin, HIGH);
}

void loop() {
  // Acende o LED
  delay(100); // Aguarda a estabilização da luz

  // Lê o valor da luz refletida
  int leituraLDR = analogRead(ldrPin);

  // Apaga o LED
  //digitalWrite(ledPin, LOW);

  // Converte leitura para percentagem de sujidade (0 = limpo, 100 = sujo)
  int sujidade = map(leituraLDR, valorLimpo, valorSujo, 0, 100);
  sujidade = constrain(sujidade, 0, 100); // Garante que fica entre 0 e 100

  // Exibe resultado
  Serial.print("Valor LDR: ");
  Serial.print(leituraLDR);
  Serial.print(" | Sujidade: ");
  Serial.print(sujidade);
  Serial.println("%");

  delay(1000); // Espera 1 segundo antes da próxima leitura
}
