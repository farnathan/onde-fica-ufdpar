# "Onde fica?" · Histórico e documentação do projeto

Este documento reúne tudo o que foi decidido, construído e aprendido nas conversas com o Claude
em **23 e 24 de outubro de 2026**, para que o projeto possa continuar sem o histórico do chat.

- **Site publicado:** https://farnathan.github.io/onde-fica-ufdpar/
- **Repositório:** https://github.com/farnathan/onde-fica-ufdpar (conta pessoal **farnathan**)
- **Versão atual:** 1.6 (24/10/2026) · notas de cada versão em [NOVIDADES.md](NOVIDADES.md)
- **Natureza:** protótipo independente, **não oficial**, para propor à UFDPar.

## Sumário
1. [O que é e por que existe](#1-o-que-é-e-por-que-existe)
2. [Linha do tempo](#2-linha-do-tempo)
3. [Decisões e preferências registradas](#3-decisões-e-preferências-registradas)
4. [Fontes de dados](#4-fontes-de-dados)
5. [Como o site funciona por dentro](#5-como-o-site-funciona-por-dentro)
6. [Como atualizar](#6-como-atualizar)
7. [Ferramentas de processamento](#7-ferramentas-de-processamento)
8. [Acessos, contas e publicação](#8-acessos-contas-e-publicação)
9. [Limitações conhecidas e lições aprendidas](#9-limitações-conhecidas-e-lições-aprendidas)
10. [Pendências e próximos passos](#10-pendências-e-próximos-passos)
11. [Como retomar com o Claude](#11-como-retomar-com-o-claude)

---

## 1. O que é e por que existe

**Problema.** O mapa oficial do Campus Ministro Reis Velloso
([ufdpar.edu.br/ufdpar/paginas/mapa_do_campus](https://ufdpar.edu.br/ufdpar/paginas/mapa_do_campus))
é uma imagem estática. Para o calouro, ela tem cinco dificuldades:
- o número do bloco sozinho não diz o que funciona nele;
- um mesmo bloco reúne vários setores e cursos, em andares diferentes;
- não mostra andares, rotas nem acessibilidade;
- não tem "você está aqui" nem funciona bem no celular;
- desatualiza com facilidade.

O QR code do mapa impresso aponta para a mesma página com a imagem, ou seja, não existe hoje um "mapa virtual" de verdade.

**Solução.** Um site de uma página, pensado para o celular. O aluno digita a sala, o curso, o setor ou o serviço e vê o bloco,
o andar, o caminho a pé e informações úteis (horários, contatos, regras), sobre a própria ilustração oficial do campus.

**Descoberta-chave.** A numeração das salas é **única no campus inteiro (1 a 482)** e segue a ordem dos blocos.
Basta digitar o número que está no horário ("405") para saber bloco e andar (Bloco 23, 2º andar).

---

## 2. Linha do tempo

### 23/10/2026
- **Análise inicial** do mapa oficial e levantamento de 7 caminhos de solução: índice curso/setor → bloco, sinalização física com QR,
  cadastro no Google Maps e OpenStreetMap, mapa interativo com busca, link do SIGAA para o mapa, acolhimento humano e acessibilidade.
- **v1 (protótipo):** mapa com busca sobre uma planta ilustrativa, com dados do *Cronograma do Inventário Patrimonial 2025*.
- **Mapa oficial "Localize-se!"** enviado pelo usuário (o site da UFDPar bloqueia acesso automático).
  O protótipo passou a usar a posição real dos blocos, os andares e as faixas de salas.
- **Melhorias de design escolhidas pelo usuário:** identidade UFDPar (azul, pinos vermelhos, etiquetas laranja),
  layout de app no celular (mapa em tela cheia, painel que sobe de baixo, zoom de pinça) e corte do prédio com o andar
  aceso e rota tracejada. O item "funções do calouro" (Meu horário, Você está aqui, acessibilidade) ficou **em segundo plano**.
- **Vetorização da ilustração** para servir de base ao mapa clicável. Os pinos e etiquetas originais foram apagados
  (*inpainting*) e redesenhados por cima, clicáveis.
- **Backup** da versão daquele momento: artefato "Onde Fica Backup" no Claude e um zip.
- **Novas fontes:** o usuário baixou os PDFs (Guia do Calouro, Diagnóstico da PRAE, Resoluções CONSUNI 80/2024 e 184/2026,
  UFDPar no Censo). Com eles entraram horários e regras do RU, informações da Biblioteca, serviços da PRAE e contatos do DCE.
  A lista de turmas do SIGAA foi considerada **inviável** pelo usuário.
- **Publicação no GitHub Pages** (conta pessoal farnathan): pacote com prévia de link para WhatsApp, funcionamento offline e instalação no celular.
- **Ajustes pedidos:** abrir mostrando o campus inteiro (antes abria no Bloco 23), permitir mais zoom out,
  retirar "Campus Ministro Reis Velloso" e usar o nome por extenso "Universidade Federal do Delta do Parnaíba (UFDPar)".
- **Fluxo de envio:** primeiro uma pasta no computador (`Documentos\onde-fica-ufdpar`) com o atalho `publicar.bat`.
  Depois, envio direto do Claude para o GitHub (ver seção 8). O `publicar.bat` foi **aposentado**.
- **OpenStreetMap:** a exportação da região permitiu ligar a planta a coordenadas reais (erro médio de cerca de 3 m).
  Entraram o botão "Onde estou" (GPS), o "Como chegar (Google Maps)" e a distância e o tempo a pé.
- **Google Earth:** o arquivo KML enviado veio vazio. Ficaram as instruções para desenhar os Blocos 2 a 9 e a Escola de Aplicação (pendente).
- **Bordas da planta:** primeiro preenchidas com grama, depois a área externa ficou transparente (campus como "ilha")
  e, por fim, com **fundo branco sempre**, a pedido do usuário.
- **v1.4:** busca tolerante a erros e sinônimos, planta em WebP (2,9 MB → 315 KB), contador anônimo (GoatCounter) e `NOVIDADES.md`.
- **v1.5:** mapa menos poluído (bolinhas numeradas no zoom afastado), nome ao passar o mouse, contorno real de 11 prédios,
  camadas liga/desliga, escala e norte, tela inicial organizada por necessidade.

### 24/10/2026
- **v1.6:** revisão completa com testes automáticos e 14 correções (busca, arrastar o mapa, GPS, celular deitado, acessibilidade).
- **Este documento** e a pasta `ferramentas/` com os scripts de processamento.
- **v1.6.1:** manchas sob os pinos. A limpeza antiga (TELEA) deixava um borrão com o formato do pino oficial apagado, visível acima de cada pino novo.
  Nova limpeza: cópia de amostras do próprio telhado (13 blocos) e preenchimento guiado por estrutura (7 blocos). **20 de 26 blocos sem mancha**;
  os Blocos 7, 14, 18, 21, 22 e 24 continuam com o borrão, porque os dois métodos novos pioravam esses casos.

---

## 3. Decisões e preferências registradas

| Tema | Decisão |
|---|---|
| Cabeçalho | Nome por extenso: "Universidade Federal do Delta do Parnaíba (UFDPar)". **Não** usar "Campus Ministro Reis Velloso". |
| Fundo do mapa | **Branco**, inclusive no modo escuro. O campus aparece como "ilha" de contorno irregular (alisado). |
| Abertura | O site abre mostrando o campus inteiro, sem bloco selecionado. `#bloco-XX` só aparece quando alguém escolhe um lugar. |
| Base do mapa | Ilustração oficial "Localize-se!", limpa, com pinos, etiquetas e ícones redesenhados por cima. |
| Conta do GitHub | Repositório na conta **pessoal** farnathan. A conta da empresa (produtos-ecoadventure) é só colaboradora, para o Claude enviar. |
| Envio | Direto do Claude para o GitHub. **Não usar mais o `publicar.bat`**, porque a pasta local está desatualizada. |
| SIGAA | Fora do escopo (inviável obter a lista de turmas). |
| "Meu horário" | Em segundo plano. |
| Identidade | Protótipo independente, não oficial. O README e o rodapé deixam isso claro. |

---

## 4. Fontes de dados

| Fonte | O que forneceu | Observações |
|---|---|---|
| Mapa oficial "Localize-se!" (Comunicação Institucional UFDPar, designer Joanson Sousa) · [página](https://ufdpar.edu.br/ufdpar/paginas/mapa_do_campus) · cópia em `ferramentas/fontes/mapa-localize-se.jpg` | Posição dos blocos, faixas de salas, andares, setores, ícones de estacionamento e alimentação | Fonte principal. Prevalece sobre o inventário de 2025 quando há conflito. |
| [Cronograma do Inventário Patrimonial 2025](https://ufdpar.edu.br/UFDPar/realizacao-do-inventario-patrimonial-da-ufdpar-13-a-18-de-outubro-de-2025/copy_of_CronogramadeatividadeseMapadoCampusMinistroReisVelloso.pdf) | Primeira versão dos dados por bloco | Usado só na v1. Tinha turnos (M/T/N), que saíram por não estarem no mapa oficial. |
| [Guia do Calouro (Economia)](https://ufdpar.edu.br/UFDPar/paginas/time-line-academica/GuiadoCalouro.pdf) | Regras da Biblioteca, benefícios da PRAE, DCE (local, e-mail, Instagram), horário do RU | **Usa a numeração antiga das salas** (ex.: sala 135), incompatível com a atual. E-mails de setores estão no domínio antigo `@ufpi.edu.br`. Nada disso foi usado. |
| [Resolução CONSUNI nº 184/2026](https://ufdpar.edu.br/prae/paginas/ResoluoConsuni1842026.pdf) | Regulamento do RU: horários, acesso, 1 almoço + 1 jantar, sala reservada via NIA, e-mail da DAN | Revoga a Resolução 80/2024 ([link](https://ufdpar.edu.br/prae/paginas/resolucao_consuni_80de17dejunhode2024.pdf)). |
| [Diagnóstico da PRAE](https://ufdpar.edu.br/UFDPar/paginas/paginas-pdu/acompanhamento-pro-reitorias/diagnostico-pro-reitorias-paginas/diagnostico-arquivos/relatorio-diag-prae-final.pdf) | Serviços da PRAE, horário do Serviço Médico, refeitório com 149 lugares | Documento de cerca de 2022: **confirmar** o horário do Serviço Médico. |
| [UFDPar no Censo da Educação Superior](https://ufdpar.edu.br/UFDPar/AUFDParnoCensodaEducaoSuperior1.pdf) | Biblioteca: 92 assentos e itens de acessibilidade (dados de 2024) | Não traz acessibilidade por bloco. |
| OpenStreetMap (exportação da região) · `ferramentas/fontes/campus-openstreetmap.osm` | Contorno do terreno, cerca de 25 prédios, caminhos, árvores, entorno | © colaboradores do OpenStreetMap (licença ODbL; crédito no rodapé do site). **Incompleto:** faltam os Blocos 2 a 9 e a Escola de Aplicação, e os prédios não têm nome. |

**Acesso automático bloqueado:** o site da UFDPar recusa ferramentas automáticas, e o ambiente do Claude não alcança o SIGAA
nem a API do OpenStreetMap. O caminho que funciona é o usuário baixar os arquivos e enviá-los.

---

## 5. Como o site funciona por dentro

### Arquivos publicados
| Arquivo | Papel |
|---|---|
| `index.html` | A página inteira: estilos, dados e lógica, sem bibliotecas externas. Só as fontes vêm do Google Fonts. |
| `planta-campus.webp` | Base do mapa: ilustração oficial limpa, com transparência fora do campus (3300 × 3420 px, cerca de 320 KB). |
| `sw.js` | Service worker: guarda a página e a planta para funcionar com sinal fraco. Só cuida de arquivos do próprio site. |
| `manifest.webmanifest`, `icone.svg`, `icone-180.png` | Instalação na tela inicial do celular. |
| `previa.jpg` | Imagem de prévia do link (1200 × 630) para WhatsApp e redes sociais. |
| `NOVIDADES.md`, `README.md`, `HISTORICO.md` | Documentação. |
| `ferramentas/` | Scripts e fontes para regenerar a planta, os contornos e a georreferência (não vão para o site). |

### Sistema de coordenadas
Tudo no mapa usa as **unidades da planta**: as mesmas coordenadas de uma versão da imagem oficial reduzida para 2000 px de largura
(1 unidade = 4 px da imagem original). A planta ocupa x 760–1860 e y 160–1300. 1 unidade ≈ **0,293 m**.

### Dados principais (no início do `<script>` do `index.html`)
- **`B`**: os lugares. Formato de cada item:
  `[id, categoria, nome, [sala inicial, sala final], andares, [x, y, largura, altura], etiqueta?]`
  - `andares` = lista de `[andar, [salas]|null, [itens], "palavras-chave para a busca"]` (andar 0 = térreo).
  - Categorias: `aula`, `adm`, `lab`, `est`, `apoio`.
  - Lugares sem número (RU, Biblioteca, Quadra, Escola de Aplicação) usam ids `RU`, `BC`, `QE`, `EA` e uma etiqueta laranja.
- **`INFO`**: cartões extras (horários, "Bom saber", contatos e fonte) para RU, Biblioteca, Bloco 18 (PRAE) e Bloco 23 (DCE).
- **`PIN` / `TAG`**: posição de cada pino e etiqueta, nas mesmas posições do mapa oficial.
- **`OUTLINE`**: contorno real do telhado de 11 prédios. Os demais usam o retângulo de `B`.
- **`ICONS`**: 11 ícones (5 estacionamentos, 2 de motos, 1 bicicletário, 3 de alimentação), como camadas.
- **`WALK`**: os passeios do campus, como segmentos retos, usados para calcular a rota.
- **`ENTRY`**: a entrada principal, na Av. São Sebastião (ponto de partida da rota sem GPS).
- **`GEO`**: a matriz que converte a planta em GPS (seção 7).
- **`GROUPS` / `COURSES`**: a tela inicial (grupos por necessidade e atalhos dos 12 cursos).
- **`SYN` / `STOP`**: sinônimos e palavras ignoradas pela busca.

### Busca
1. Normaliza o texto (sem acentos, minúsculas). Números viram busca por faixa de salas; "bloco 12" vai direto ao bloco.
2. Ignora palavras vazias (`STOP`). Se não sobra nada útil ("onde fica", uma letra só), pede para continuar digitando e não seleciona nada.
3. Cada palavra aceita: ela mesma, o sinônimo (`SYN`), palavras parecidas do vocabulário (distância de edição 1 ou 2, a mais próxima)
   e, com 2 ou 3 letras, o começo de palavra.
4. Ordena: nome exato > palavra no nome do prédio > texto do andar > só o nome do prédio. Correções de digitação ficam abaixo.
   Andares que só batem pelo nome do prédio viram um resultado por prédio.
5. Seleciona o primeiro resultado, enquadra o mapa e grava `#bloco-XX` no endereço.

### Rota
É o caminho mais curto (Dijkstra) pelos segmentos de `WALK`, da entrada principal (ou da posição do GPS) até o ponto de passeio mais próximo do prédio.
A distância usa 0,293 m por unidade, e o tempo considera 1,2 m/s. O caminho é aproximado.

### GPS e "Como chegar"
- `planToLL` e `llToPlan` convertem entre planta e latitude/longitude pela matriz `GEO`.
- "Onde estou" usa `watchPosition`. Fora da área do campus, a página mostra um aviso e sugere o Google Maps.
  **Só funciona no site publicado**: dentro do artefato do Claude, o navegador bloqueia a localização.
- "Como chegar" abre `google.com/maps/dir/?api=1&destination=LAT,LON&travelmode=walking` com o centro do prédio.

### Mapa
- Zoom e arrasto próprios (roda do mouse, pinça, botões). O centro da vista não sai da área do campus.
- Os pinos têm tamanho fixo na tela. Com o zoom bem afastado, viram bolinhas numeradas, e as etiquetas dos setores só aparecem ao aproximar.
- Camadas (estacionamentos, motos e bicicletas, alimentação, nomes dos setores) ficam salvas no navegador (`localStorage`).
- No celular deitado (altura até 500 px), o painel fica ao lado do mapa.

### Outros
- **Status do RU** ("servindo / aberto / fechado") pelo horário de Parnaíba (UTC−3). **Não considera feriados nem recesso.**
- **Contador:** GoatCounter, código `onde-fica-ufdpar`. Só liga em `*.github.io` e conta visitas, buscas, lugares, "Como chegar" e "Onde estou",
  sem cookies.
- **Links diretos:** `…/onde-fica-ufdpar/#bloco-23`, `#bloco-ru`, `#bloco-bc`, `#bloco-qe`, `#bloco-ea`. Servem para os QR codes.

---

## 6. Como atualizar

> Ao pedir mudanças ao Claude, ele mesmo edita, testa e envia ao GitHub. Os passos abaixo servem para fazer à mão ou para conferir.

- **Mudou o que funciona numa sala ou num bloco:** em `B`, edite os `itens` e as `palavras-chave` do andar certo.
- **Novo horário, regra ou contato:** acrescente ou edite a entrada do lugar em `INFO` e preencha `src` com a fonte.
- **A busca não acha um apelido:** inclua em `SYN` (`"apelido":"palavra que existe nos dados"`).
- **Mudar a tela inicial:** edite `GROUPS` (`[id, andar, título, subtítulo]`) e `COURSES` (`[rótulo, termo de busca]`).
- **Trocar a planta:** gere uma nova com `ferramentas/limpar_planta.py`, substitua `planta-campus.webp` e **mude o `?v=`** no `index.html` e no `sw.js`
  (ex.: `planta-campus.webp?v=1.7`), senão os navegadores continuam mostrando a antiga.
- **Toda publicação:** aumente a versão do cache no `sw.js` (`const C="onde-fica-vNN"`) e registre a mudança no `NOVIDADES.md`.
- **Publicar:** envie para a branch `main`. O GitHub Pages atualiza em 1 a 2 minutos. Se o navegador mostrar a versão antiga, use Ctrl+Shift+R.

---

## 7. Ferramentas de processamento

Pasta `ferramentas/` (requer `pip install opencv-python-headless numpy`; `exemplar.py` e `estrutura.py` são módulos usados pelo `limpar_planta.py`):

| Script | O que faz | Saída |
|---|---|---|
| `limpar_planta.py` | Recorta a planta da imagem oficial, detecta e guarda os ícones, apaga pinos, etiquetas e ícones (*inpainting*: TELEA como base; cópia de amostras nos telhados contínuos e preenchimento guiado por estrutura nos pinos que cobriam bordas, só nos blocos das listas `REFAZER` e `ESTRUTURA`), deixa transparente a área fora da ilustração e estende a avenida | `saida/planta-campus.webp`, `dados/icones.json`, `dados/planta-limpa.png` |
| `contornos.py` | Recorta o contorno do telhado de 11 prédios pela cor (branco ou telha) | `dados/contornos.json` (constante `OUTLINE`) |
| `georreferencia.py` | Ajusta a planta às coordenadas reais pelos prédios do OpenStreetMap (mínimos quadrados) | `dados/georef.json` (constante `GEO`) |

Os três foram conferidos: reproduzem exatamente a planta e os contornos publicados.
**Atenção (v1.6.1):** o `contornos.json` publicado foi gerado com a planta antiga. Rodar o `contornos.py` com a planta nova muda o contorno do
Bloco 14 (a borda do Auditório desce sobre os Blocos 12 e 13, errado) e mexe 6 unidades num canto da BC. Por isso o `contornos.json` não foi regerado.
A matriz recalculada difere da usada no site em menos de 1 m, porque o site usou caixas arredondadas.

**Aprendizados do processamento:**
- Os ícones precisam ser detectados na imagem **original**, antes de apagar os pinos. Senão a limpeza "puxa" a cor dos ícones vizinhos e deixa manchas cor-de-rosa.
- A primeira camada da vetorização em SVG (bege `#C8C6BB`) também é a cor das calçadas. Trocá-la apaga as calçadas.
- No miolo cinza (Blocos 2 a 17), telhados e pátios têm a mesma cor, então o recorte automático não separa os prédios.
- O TELEA borra a partir da borda: em telhado com textura, vira uma mancha com o formato do pino apagado, maior que o pino novo.
  Copiar amostras na **vertical** (mesmas colunas) preserva telhas e cumeeiras; copiar livremente ou em cruz entorta as linhas e puxa grama para o telhado.
  Onde o pino cobria uma borda, é preciso primeiro reconstruir onde fica cada área (telhado, grama, calçada) e só depois preencher cada uma com a própria textura.
- A solução definitiva continua sendo pedir à Comunicação Institucional o arquivo original da ilustração **sem pinos**.

---

## 8. Acessos, contas e publicação

**GitHub Pages:** repositório público `farnathan/onde-fica-ufdpar`. Settings → Pages → *Deploy from a branch* → `main` / raiz.

**Envio direto pelo Claude** (configurado em 23/10/2026):
1. A conta da empresa **produtos-ecoadventure** foi adicionada como **colaboradora** do repositório (convite aceito).
2. O **app do Claude para GitHub** foi instalado na conta **farnathan**, com acesso **só** a este repositório.

Para revogar: em `Settings → Collaborators` do repositório, remova produtos-ecoadventure, e/ou em
`Settings → Applications → Installed GitHub Apps` da conta farnathan, remova o app do Claude.
Atenção: quem tiver acesso à conta da empresa também pode alterar este repositório enquanto ela for colaboradora.

**`publicar.bat` (aposentado):** ficava em `Documentos\onde-fica-ufdpar` e enviava com o login pessoal
(`https://farnathan@github.com/...`, para o Windows não usar o login salvo da empresa). Como o Claude agora envia direto,
essa pasta ficou desatualizada. **Não rode o atalho**, porque ele tentaria enviar arquivos antigos.

**GoatCounter:** criar a conta em goatcounter.com com o código **`onde-fica-ufdpar`**. Os números aparecem em
`onde-fica-ufdpar.goatcounter.com`. Até 24/10/2026 não havia confirmação de que a conta foi criada.

**Artefatos no Claude** (cópias de visualização, sem GPS):
- Principal: https://claude.ai/artifact/5uYFUoKkyNPJ6ipC2ENhqN
- Backup congelado da manhã de 23/10 (privado): https://claude.ai/artifact/HNoG45ozBn5tGs7ZFMwRre

---

## 9. Limitações conhecidas e lições aprendidas

**Do site**
- Contorno exato só em 11 prédios. Os Blocos 2 a 17 e o 18 usam retângulos.
- A precisão do GPS é menor no lado da Av. Pinheiro Machado (Blocos 2 a 9), que não existe no OpenStreetMap.
- As rotas seguem passeios traçados à mão e terminam no ponto de passeio mais próximo, não na porta do prédio.
- O status do RU não considera feriados nem recesso.
- O horário do Serviço Médico é de cerca de 2022.
- Ainda não há dados de banheiros, rampas e elevadores por bloco.
- Ainda há mancha dos pinos oficiais apagados nos Blocos 7, 14, 18, 21, 22 e 24.

**Do processo**
- **Gravação no computador do usuário:** a ferramenta do Claude reaproveitou versões antigas quando o mesmo caminho de origem era usado de novo.
  Solução: usar um caminho novo a cada envio e trazer os arquivos de volta para conferir antes de avisar.
- **Cache do navegador:** trocar uma imagem sem mudar o nome faz o navegador mostrar a antiga. Use `?v=` no endereço da imagem.
- **Login do Git no Windows:** o Gerenciador de Credenciais usa o login salvo (o da empresa). Com o usuário no endereço do repositório, ele separa os logins.
- **Fontes da UFDPar:** o site bloqueia acesso automático, então o usuário precisa baixar e enviar os documentos.

---

## 10. Pendências e próximos passos

**Prioridade alta**
- [ ] **Manchas restantes** (Blocos 7, 14, 18, 21, 22 e 24): retoque manual com carimbo/correção (ex.: Photopea) em `planta-campus.webp`,
      ou a ilustração sem pinos da UFDPar. Se retocar à mão, subir a versão `?v=` no `index.html` e no `sw.js`.
- [ ] **Criar a conta no GoatCounter** (`onde-fica-ufdpar`). Sem ela, o site não conta nada.
- [ ] **Placas com QR code por bloco:** PDF para gráfica, com links `#bloco-XX`.
- [ ] **Página de proposta para a UFDPar** (Comunicação Institucional, PREG, PRAE): problema, site, números de uso, o que precisam fornecer e o pedido da ilustração sem pinos.
- [ ] **Instruções da rota em texto**, passo a passo.
- [ ] **Botão "Informar erro"** em cada lugar.

**Dados (dependem de coleta)**
- [ ] Desenhar os Blocos 2 a 9 e a Escola de Aplicação no Google Earth (projeto KML, um polígono com nome por prédio) para melhorar o GPS.
      O primeiro KML enviado veio vazio.
- [ ] Página de coleta em campo para marcar a **porta** de cada prédio.
- [ ] Banheiros, rampas e elevadores por bloco.
- [ ] Confirmar o horário do Serviço Médico com a PRAE.
- [ ] Horários de PREG, PRAE, coordenações, xérox e cantinas (para o "aberto agora").
- [ ] Opcional: cadastrar nomes e números dos blocos no OpenStreetMap, para aparecerem também no Organic Maps e no OsmAnd.

**Funções**
- [ ] "Meu curso" (kit do calouro por curso).
- [ ] Botão "Compartilhar" e buscas recentes.
- [ ] Dados separados num `dados.json`, com a data de cada informação.
- [ ] Feriados e recesso no status do RU.
- [ ] "Meu horário" (estava em segundo plano).
- [ ] Teste com 5 a 10 calouros.

---

## 11. Como retomar com o Claude

Em uma conversa nova, cole algo como:

> Estou continuando o projeto "Onde fica?", um mapa interativo do campus da UFDPar publicado em
> https://farnathan.github.io/onde-fica-ufdpar/ (repositório farnathan/onde-fica-ufdpar).
> Leia o HISTORICO.md e o NOVIDADES.md do repositório antes de começar.
> A conta produtos-ecoadventure é colaboradora e o app do Claude está instalado na minha conta, então você pode enviar direto para a main.
> Quero agora: [descreva a próxima tarefa].

Dicas:
- Peça para ele **testar antes de publicar** (celular e computador, claro e escuro) e para **atualizar o NOVIDADES.md**.
- Para dados novos da UFDPar, baixe os PDFs e anexe na conversa.
- O documento-mestre de dados é o próprio `index.html` (constantes `B`, `INFO`, `GROUPS`, `SYN`).
