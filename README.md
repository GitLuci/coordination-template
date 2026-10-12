# Molde de coordenação

Uma forma de trabalhar com **um coordenador e dois ou mais developers** (por exemplo, um de frontend e um de
backend), cada um no seu terminal ou sessão de agente. Não depende de nenhum projecto, linguagem ou fornecedor de IA.

A ideia em três frases:

1. **Contrato antes de código.** FE e BE só começam a implementar depois de assinarem o contrato da API (o que o FE
   envia, o que o BE recebe e devolve, o que o FE recebe, os erros e exemplos). Os dois lados testam contra os mesmos
   exemplos, por isso a integração não traz surpresas.
2. **O coordenador decide, os devs implementam.** O coordenador responde às perguntas no lugar do dono, gere a fila de
   testes e integra. Só sobe ao dono o que é mesmo dele: arquitectura, âmbito do produto, custos e acções
   irreversíveis ou para fora.
3. **Tudo o que importa fica escrito.** Quadro, perguntas, decisões e contrato vivem em ficheiros que todos lêem;
   ninguém depende da memória de uma conversa.

## Por onde começar

| Ficheiro | Para quê |
|---|---|
| [`MOLDE.md`](MOLDE.md) | O método completo: papéis, comunicação, ciclo de uma tarefa, testes, escalamento |
| [`AGENTS.md`](AGENTS.md) | Ponto de entrada para qualquer agente que abra o projecto (copiar para cada repo) |
| [`papeis/`](papeis/) | O que cada papel faz e não faz: coordenador, dev BE, dev FE |
| [`contrato/`](contrato/) | O processo contract-first, o modelo do contrato e a verificação de versões |
| [`coordenacao/`](coordenacao/) | Modelos do quadro, perguntas, decisões, fila de testes e caixas de mensagens |
| [`gates/QUALITY-GATE.md`](gates/QUALITY-GATE.md) | O que tem de passar antes de uma tarefa ser integrada |
| [`prompts/`](prompts/) | Prompts de arranque para colar no terminal de cada papel |

## Como aplicar a um projecto

**Um só repositório (monorepo):** copia `AGENTS.md`, `coordenacao/`, `contrato/` e `gates/` para a raiz do projecto.

**Repositórios separados (FE e BE):** a coordenação fica num sítio que os três lêem e escrevem:

- uma pasta local partilhada (ex.: `../coordenacao-<projecto>/`) ou um repositório próprio de coordenação, com
  `coordenacao/` e `contrato/`;
- cada repositório (FE e BE) tem o seu `AGENTS.md` a apontar para essa pasta e uma cópia do contrato assinado em
  `contrato/`, verificada pelo `scripts/contrato.py verificar --contra <pasta partilhada>`.

Depois, preenche os prompts de [`prompts/`](prompts/) com os dados do projecto e cola-os em cada terminal.

## Comunicação entre agentes

- **Sessões do Claude Code na mesma máquina** podem usar as mensagens directas entre sessões para avisos urgentes.
  Mesmo assim, o que for decidido fica escrito nos ficheiros.
- **Terminais, sessões ou agentes de outros fornecedores** (ou qualquer mistura) comunicam **só por ficheiros**, no
  git ou numa pasta local partilhada: o quadro, as caixas de mensagens, as perguntas e as decisões.
