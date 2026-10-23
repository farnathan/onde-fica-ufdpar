# Onde fica? · UFDPar

Mapa interativo do Campus Ministro Reis Velloso (UFDPar) para ajudar calouros a se localizar.
Digite o número da sala, o curso, o setor ou o serviço e veja o bloco, o andar e o caminho desde a entrada principal.

**Protótipo independente, não oficial.** Dados e base do mapa a partir do mapa "Localize-se!" da Coordenadoria de
Comunicação Institucional da UFDPar, do Guia do Calouro, da Resolução CONSUNI nº 184/2026, do Diagnóstico da PRAE
e do documento "UFDPar no Censo da Educação Superior".

## Arquivos
- `index.html` — a página (dados dos blocos ficam no início do `<script>`)
- `planta-campus.svg` — base do mapa (ilustração oficial vetorizada, sem pinos)
- `sw.js`, `manifest.webmanifest`, `icone.svg` — funcionamento offline e instalação no celular

## Publicar
Site estático: basta servir a pasta. No GitHub Pages: Settings → Pages → Deploy from a branch → `main` / raiz.
Abrir direto num bloco: `…/#bloco-23`.
