# Onde fica? · UFDPar

Mapa interativo do campus da Universidade Federal do Delta do Parnaíba (UFDPar) para ajudar calouros a se localizar.
Digite o número da sala, o curso, o setor ou o serviço e veja o bloco, o andar e o caminho desde a entrada principal.

**Protótipo independente, não oficial.** Dados e base do mapa a partir do mapa "Localize-se!" da Coordenadoria de
Comunicação Institucional da UFDPar, do Guia do Calouro, da Resolução CONSUNI nº 184/2026, do Diagnóstico da PRAE
e do documento "UFDPar no Censo da Educação Superior".

## Arquivos
- `index.html` — a página (dados dos blocos ficam no início do `<script>`)
- `planta-campus.webp` — base do mapa (ilustração oficial limpa, sem pinos; 332 KB)
- `sw.js`, `manifest.webmanifest`, `icone.svg` — funcionamento offline e instalação no celular
- `tipografia/` — fonte Hind (licença livre OFL, em `OFL.txt`), usada no lugar da Frutiger do manual de identidade da UFDPar

## Publicar
Site estático: basta servir a pasta. No GitHub Pages: Settings → Pages → Deploy from a branch → `main` / raiz.
Abrir direto num bloco: `…/#bloco-23`.

## Documentação
- [HISTORICO.md](HISTORICO.md): histórico do projeto, decisões, fontes, como o site funciona, como atualizar e pendências.
- [NOVIDADES.md](NOVIDADES.md): notas de cada versão.
- `ferramentas/`: scripts para regenerar a planta, os contornos dos prédios e a georreferência.
