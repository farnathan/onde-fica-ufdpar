# Novidades do "Onde fica?"

Histórico de atualizações do mapa interativo do campus da Universidade Federal do Delta do Parnaíba (UFDPar).
A versão mais recente fica no topo.

---

## Versão 1.7.2 · 24/10/2026

**Correções**
- O destaque do Auditório (Bloco 14) e da Biblioteca Central agora segue o telhado. Antes as bordas saíam tortas e invadiam a calçada e os prédios vizinhos.
- Os destaques dos Blocos 1, 22 e 23 e da Escola de Aplicação também ficaram retos.

---

## Versão 1.7.1 · 24/10/2026

**Correções**
- Menos manchas no mapa: o telhado do Auditório (Bloco 14) e os Blocos 22 e 24 ficaram limpos, assim como as áreas sob 7 etiquetas e 5 ícones. A reconstrução agora usa o contorno real de cada prédio, tirado do OpenStreetMap.
- Ainda há mancha nos Blocos 7, 18 e 21 e em três áreas pequenas.

---

## Versão 1.7 · 24/10/2026

**Visual**
- Novas cores e tipografia, seguindo o Manual de Identidade Visual da UFDPar: azul-marinho institucional no cabeçalho com filete dourado, pinos no vermelho do manual e etiquetas no azul do manual.
- Letra mais sóbria e legível (Hind, da mesma família de desenho da Frutiger usada pela universidade), cantos menos arredondados e sem sombras pesadas.
- A fonte agora vem do próprio site: abre mais rápido e não depende mais do Google.
- Novo ícone e nova imagem de prévia quando o link é compartilhado.

---

## Versão 1.6.2 · 24/10/2026

**Privacidade**
- O GPS agora desliga sozinho: quando você sai do campus, depois de 10 minutos ou enquanto a página não está na tela (volta quando você reabre).
- Um segundo toque no botão de localização desliga o GPS. O botão fica azul enquanto ele está ligado.
- Buscas que não acham nenhum lugar são contadas sem o texto digitado.
- O rodapé explica que a sua localização só é usada no seu aparelho e não é enviada nem guardada.

---

## Versão 1.6.1 · 24/10/2026

**Correções**
- Acabaram as manchas acima dos pinos em 20 dos 26 blocos. Eram restos dos pinos do mapa oficial, que foram apagados da ilustração e deixavam um borrão no telhado. Agora o telhado é refeito com a textura dele mesmo.
- Ainda há mancha nos Blocos 7, 14, 18, 21, 22 e 24. Fica para uma próxima versão.

---

## Versão 1.6 · 24/10/2026

**Correções**
- Buscas sem conteúdo útil ("onde fica", uma letra só) não selecionam mais o Bloco 1 sozinhas. A página pede para continuar digitando.
- A busca já encontra resultados com 2 ou 3 letras: "bib" acha a Biblioteca, "pre" acha a PREG.
- Ao buscar uma palavra que está no nome do prédio, ele aparece antes dos que só a mencionam.
- Depois de "Ver todos os lugares", o botão "Limpar" e o novo "← Voltar ao início" retornam à tela inicial.
- O mapa não pode mais ser arrastado para fora da tela.
- O ponto azul do GPS tem tamanho fixo na tela; antes ficava quase invisível com o zoom afastado.
- As atualizações do GPS não redesenham mais o painel inteiro.
- A etiqueta da Biblioteca não cobre mais o pino do Bloco 15.

**Celular**
- Com o celular deitado, o painel de busca fica ao lado do mapa, em vez de cobrir a maior parte dele.
- Em telas pequenas e com o zoom afastado, as etiquetas laranja e os ícones ficam menores e não escondem os pinos.

**Acessibilidade**
- A busca é o primeiro item ao navegar com Tab (antes eram 36 Tabs até ela).
- Esc fecha o painel de camadas.
- O leitor de tela anuncia só um resumo curto ("Bloco 23, 2º andar selecionado no mapa"), em vez de reler o painel inteiro.
- RU, Biblioteca, Quadra e Escola de Aplicação ganharam ícones na lista, no lugar das siglas.

**Por dentro**
- O modo offline deixou de interferir em arquivos de outros sites (fontes, contador).
- Planta antiga em SVG (2,9 MB) removida do repositório.

---

## Versão 1.5 · 23/10/2026

**Mapa mais limpo**
- Com o zoom afastado, os blocos viram bolinhas numeradas e os nomes dos setores (Clínicas, PREUNI, Auditório Central…) só aparecem ao aproximar.
- Pinos com tamanho constante na tela e área de toque maior no celular.
- No computador, passar o mouse sobre um prédio mostra o nome do bloco.

**Prédios com contorno real**
- O destaque amarelo do prédio escolhido segue o formato real do telhado em 11 prédios (Blocos 1, 14, 19 a 24, RU, Biblioteca e Escola de Aplicação).
- Contorno do Bloco 17 corrigido.

**Camadas**
- Novo botão de camadas: liga e desliga estacionamentos, motos e bicicletas, alimentação e nomes dos setores. A escolha fica salva no celular.

**Escala e norte**
- Barra de escala em metros, que muda com o zoom, e indicador de norte.

**Tela inicial por necessidade**
- Em vez da lista de 41 lugares, a tela inicial agrupa: Onde comer, Atendimento ao estudante, Saúde e bem-estar, Estudar, Serviços e eventos.
- Atalhos de "Salas de aula por curso" para os 12 cursos.
- O RU mostra na própria lista se está servindo, aberto ou fechado.
- A lista completa continua em "Ver todos os lugares".

---

## Versão 1.4 · 23/10/2026

**Busca mais esperta**
- Entende erros de digitação: "biblioteka", "pedagojia", "fizioterapia" e "medicna" encontram o lugar certo.
- Entende sinônimos e apelidos: "bandejão", "lanchonete", "secretaria", "dentista", "xerox", "wifi", "adm", "fisio".
- Quando corrige uma palavra, avisa na contagem de resultados ("mostrando também …").
- Resultados mais organizados: o andar em que a coisa fica de fato aparece primeiro, e os outros andares do mesmo prédio não poluem a lista.

**Mais leve no celular**
- A planta do campus passou de 2,9 MB para 315 KB e ficou mais nítida, com a textura real dos telhados e das árvores.

**Contador de uso**
- O site passa a contar visitas, buscas e lugares escolhidos, de forma anônima e sem cookies (GoatCounter).

**Notas de atualização**
- Este arquivo, com link "Novidades" no rodapé do painel de busca.

---

## Versão 1.3 · 23/10/2026

**GPS e rotas**
- Botão **"Onde estou"**: mostra um ponto azul na planta e traça a rota a partir de onde a pessoa está. Funciona no site publicado.
- Botão **"Como chegar (Google Maps)"** em cada lugar, com a rota a pé até o prédio.
- Distância e tempo a pé em cada rota, por exemplo "290 m · 4 min a pé".
- Coordenadas ajustadas com os dados do OpenStreetMap (erro médio de cerca de 3 m).

**Planta**
- Bordas brancas da ilustração preenchidas com grama e a Av. São Sebastião estendida até o canto.
- Fundo verde fora da planta e emenda da borda corrigida.

---

## Versão 1.2 · 23/10/2026

**Site próprio**
- Publicado no GitHub Pages, com prévia do link (imagem, título e descrição) para WhatsApp e redes sociais.
- Funciona com sinal fraco depois da primeira visita e pode ser instalado na tela inicial do celular.
- Link direto para um bloco: `…/onde-fica-ufdpar/#bloco-23`.

**Ajustes**
- A página abre mostrando o campus inteiro, sem selecionar nenhum bloco.
- Zoom out até ver o campus todo.
- Nome por extenso da universidade no cabeçalho.

---

## Versão 1.1 · 23/10/2026

**Informações úteis**
- **Restaurante Universitário:** horários, regras de acesso e aviso de "servindo agora / aberto / fechado" (Resolução CONSUNI nº 184/2026).
- **Biblioteca Central:** assentos, regras de empréstimo e itens de acessibilidade (Censo da Educação Superior 2024).
- **PRAE:** serviços, benefícios e contato da Divisão de Alimentação.
- **DCE:** contato e emissão da carteira estudantil.
- Novas buscas: "médico", "dentista", "carteirinha", "cardápio", "DCE".

---

## Versão 1.0 · 23/10/2026

**Primeira versão**
- Mapa clicável sobre a ilustração oficial "Localize-se!", com os 26 blocos, RU, Biblioteca, Quadra e Escola de Aplicação.
- Busca por número de sala (1 a 482), curso, setor ou serviço.
- Corte do prédio mostrando o andar certo e caminho tracejado desde a entrada principal.
- Layout de app no celular: planta em tela cheia e painel de busca que sobe de baixo.

---

### Fontes dos dados
Mapa "Localize-se!" (Comunicação Institucional UFDPar) · Guia do Calouro · Resolução CONSUNI nº 184/2026 ·
Diagnóstico da PRAE · UFDPar no Censo da Educação Superior · © colaboradores do OpenStreetMap.

*Protótipo independente, não oficial.*
