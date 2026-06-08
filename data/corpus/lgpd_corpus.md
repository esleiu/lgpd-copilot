# Corpus LGPD para RAG

Este corpus reune trechos essenciais e explicacoes operacionais sobre a Lei Geral de Protecao de Dados Pessoais (LGPD), Lei 13.709/2018, com foco em perguntas de desenvolvimento de software, produto e governanca de dados. Ele foi estruturado para um assistente RAG citar artigos, recuperar contexto e orientar decisoes de projeto sem substituir avaliacao juridica formal.

Fonte oficial de validacao: Planalto, Lei 13.709/2018. Fonte complementar de boas praticas: ANPD, guias e orientacoes publicas.

## Pagina 1 - Objetivo e escopo

Art. 1. Esta Lei dispoe sobre o tratamento de dados pessoais, inclusive nos meios digitais, por pessoa natural ou por pessoa juridica de direito publico ou privado, com o objetivo de proteger os direitos fundamentais de liberdade e de privacidade e o livre desenvolvimento da personalidade da pessoa natural.

Para software, isso significa que qualquer sistema que colete, armazene, processe, compartilhe ou exclua dados pessoais deve ter finalidade clara, base legal, controles de seguranca e transparencia para o titular. A LGPD nao e apenas uma regra de privacidade no cadastro; ela influencia logs, analytics, CRM, atendimento, marketing, IA, integracoes, backups e retencao.

Perguntas que precisam de RAG neste corpus geralmente envolvem escolher base legal, avaliar risco de armazenamento, identificar direitos do titular, justificar retencao e definir medidas de seguranca.

## Pagina 2 - Fundamentos

Art. 2. A disciplina da protecao de dados pessoais tem como fundamentos o respeito a privacidade, a autodeterminacao informativa, a liberdade de expressao, de informacao, de comunicacao e de opiniao, a inviolabilidade da intimidade, da honra e da imagem, o desenvolvimento economico e tecnologico, a inovacao, a livre iniciativa, a livre concorrencia, a defesa do consumidor e os direitos humanos.

Na pratica, esses fundamentos orientam decisoes de produto: coletar menos dados, explicar o uso de forma compreensivel, evitar tratamento abusivo e dar ao usuario controle real. Um sistema pode ser tecnicamente correto e ainda assim problemático se usa dados de modo inesperado ou excessivo.

## Pagina 3 - Aplicacao territorial

Art. 3. A LGPD aplica-se a qualquer operacao de tratamento realizada por pessoa natural ou por pessoa juridica, independentemente do meio, do pais de sua sede ou do pais onde estejam localizados os dados, desde que a operacao de tratamento seja realizada no Brasil, tenha por objetivo a oferta ou fornecimento de bens ou servicos a individuos localizados no Brasil, ou os dados pessoais tenham sido coletados no Brasil.

Isso afeta SaaS estrangeiro, APIs hospedadas fora do Brasil e servicos de nuvem. Se o produto atende usuarios no Brasil ou coleta dados no Brasil, a LGPD pode se aplicar mesmo com infraestrutura internacional.

## Pagina 4 - Definicoes principais

Art. 5. Para os fins desta Lei, considera-se dado pessoal a informacao relacionada a pessoa natural identificada ou identificavel. Dado pessoal sensivel inclui dado sobre origem racial ou etnica, conviccao religiosa, opiniao politica, filiaçao a sindicato ou organizacao de carater religioso, filosofico ou politico, dado referente a saude ou vida sexual, dado genetico ou biometrico, quando vinculado a uma pessoa natural.

O artigo tambem define tratamento como toda operacao realizada com dados pessoais, incluindo coleta, producao, recepcao, classificacao, utilizacao, acesso, reproducao, transmissao, distribuicao, processamento, arquivamento, armazenamento, eliminacao, avaliacao, controle, modificacao, comunicacao, transferencia, difusao ou extracao.

Em sistemas, quase tudo que manipula dados de usuario e tratamento: salvar CPF, consultar historico, gerar score, gravar IP, enviar e-mail, manter log com identificador, exportar relatorio e treinar modelo com dados pessoais.

## Pagina 5 - Principios do tratamento

Art. 6. As atividades de tratamento de dados pessoais devem observar boa-fe e principios como finalidade, adequacao, necessidade, livre acesso, qualidade dos dados, transparencia, seguranca, prevencao, nao discriminacao, responsabilizacao e prestacao de contas.

Finalidade exige que o objetivo seja legitimo, especifico e informado. Adequacao exige compatibilidade entre uso e finalidade. Necessidade exige limitacao ao minimo necessario. Transparencia exige informacoes claras. Seguranca exige medidas tecnicas e administrativas. Responsabilizacao exige demonstrar conformidade.

Exemplo: pedir CPF para emitir nota fiscal pode ser adequado; pedir CPF para baixar um e-book gratuito sem justificativa pode violar necessidade. Guardar dados indefinidamente sem criterio pode violar finalidade e necessidade.

## Pagina 6 - Bases legais para dados pessoais

Art. 7. O tratamento de dados pessoais somente pode ser realizado em hipoteses como consentimento do titular, cumprimento de obrigacao legal ou regulatoria, execucao de politicas publicas, realizacao de estudos por orgao de pesquisa, execucao de contrato ou procedimentos preliminares relacionados a contrato, exercicio regular de direitos, protecao da vida ou incolumidade fisica, tutela da saude, legitimo interesse do controlador ou de terceiro, e protecao do credito.

Para desenvolvimento de software, a base legal deve ser escolhida antes da coleta. Consentimento nao e a unica base e nem sempre e a melhor. Execucao de contrato pode justificar dados necessarios para entregar o servico. Obrigacao legal pode justificar dados fiscais. Legitimo interesse exige avaliacao de expectativa do titular, necessidade e salvaguardas.

Uma resposta segura deve sempre dizer qual base legal parece aplicavel, quais dados sao necessarios e quais limites precisam ser observados.

## Pagina 7 - Consentimento

Art. 8. O consentimento deve ser fornecido por escrito ou por outro meio que demonstre manifestacao de vontade do titular. O consentimento deve referir-se a finalidades determinadas, e autorizacoes genericas para tratamento de dados pessoais sao nulas.

Consentimento precisa ser especifico, destacado e revogavel. Checkbox pre-marcado, termos genericos ou autorizacao escondida em texto longo sao ruins. O sistema deve registrar quando, como e para qual finalidade o consentimento foi dado.

## Pagina 8 - Dados sensiveis

Art. 11. O tratamento de dados pessoais sensiveis somente pode ocorrer em hipoteses especificas, como consentimento especifico e destacado, cumprimento de obrigacao legal, politicas publicas, estudos por orgao de pesquisa, exercicio regular de direitos, protecao da vida, tutela da saude, prevencao a fraude e seguranca do titular em processos de identificacao e autenticacao.

Dados sensiveis exigem maior cautela. Biometria, dados de saude e dados geneticos demandam minimizacao, protecao reforcada, controle de acesso e registro de justificativa. Em muitos casos, e melhor evitar a coleta se nao houver necessidade forte.

## Pagina 9 - Direitos do titular

Art. 18. O titular dos dados pessoais tem direito a obter do controlador confirmacao da existencia de tratamento, acesso aos dados, correcao de dados incompletos, inexatos ou desatualizados, anonimizacao, bloqueio ou eliminacao de dados desnecessarios, excessivos ou tratados em desconformidade, portabilidade, informacao sobre compartilhamento, informacao sobre possibilidade de nao consentir e revogacao do consentimento.

Um produto precisa ter processo para responder solicitacoes de titular. Mesmo que a interface nao implemente tudo automaticamente, deve existir fluxo operacional, prazo interno, registro da solicitacao e capacidade de localizar dados do usuario.

## Pagina 10 - Termino do tratamento

Art. 15. O termino do tratamento de dados pessoais ocorre em hipoteses como verificacao de que a finalidade foi alcancada, fim do periodo de tratamento, comunicacao do titular para revogacao do consentimento, ou determinacao da autoridade nacional.

Art. 16. Os dados pessoais serao eliminados apos o termino do tratamento, autorizada a conservacao para cumprimento de obrigacao legal ou regulatoria, estudo por orgao de pesquisa, transferencia a terceiro respeitados os requisitos legais, ou uso exclusivo do controlador com anonimização, vedado acesso por terceiro.

Para engenharia, isso exige politica de retencao. Backups, logs e bases analiticas tambem devem ser pensados. A resposta nao deve prometer eliminacao imediata absoluta se houver obrigacao legal de retenção.

## Pagina 11 - Agentes de tratamento

Art. 37. O controlador e o operador devem manter registro das operacoes de tratamento de dados pessoais que realizarem, especialmente quando baseado no legitimo interesse.

Controlador decide finalidades e meios; operador trata dados em nome do controlador. Contratos com fornecedores, processadores de pagamento, CRM e provedores de e-mail devem deixar papeis claros. Logs de processamento, inventario de dados e registro de bases legais ajudam na prestacao de contas.

## Pagina 12 - Seguranca e incidentes

Art. 46. Os agentes de tratamento devem adotar medidas de seguranca, tecnicas e administrativas aptas a proteger os dados pessoais de acessos nao autorizados e de situacoes acidentais ou ilicitas de destruicao, perda, alteracao, comunicacao ou difusao.

Art. 48. O controlador devera comunicar a autoridade nacional e o titular sobre a ocorrencia de incidente de seguranca que possa acarretar risco ou dano relevante aos titulares.

Medidas tecnicas incluem criptografia, controle de acesso, segregacao de ambientes, logs de auditoria, gestao de segredo, revisao de permissoes, backup seguro, monitoramento e plano de resposta a incidentes. Um app que armazena CPF ou dados sensiveis precisa justificar por que coleta, limitar acesso, proteger em repouso e em transito, e ter processo de incidente.

## Pagina 13 - Cenarios de desenvolvimento

Cenario CPF em cadastro: pode ser tratado quando necessario para contrato, obrigacao legal, antifraude ou identificacao. Se for apenas conveniencia, a coleta pode ser excessiva. Deve haver minimizacao, protecao e finalidade clara.

Cenario logs: logs podem conter IP, e-mail, identificadores e eventos de uso. Devem ter retencao definida, acesso restrito e mascaramento quando possivel.

Cenario IA generativa: prompts podem conter dados pessoais. E recomendavel evitar envio de dados sensiveis, aplicar mascaramento, controlar fornecedores e manter registro de finalidade.

Cenario marketing: comunicacao promocional pode envolver consentimento ou legitimo interesse, mas precisa respeitar expectativa do titular, opt-out e transparencia.

## Pagina 14 - Perguntas de teste para RAG

1. Posso armazenar CPF de clientes para emitir nota fiscal e prevenir fraude?
2. Quais direitos o usuario tem se pedir acesso ou exclusao dos dados?
3. Que medidas tecnicas devo aplicar se meu app guarda dados de saude?
4. Quando posso manter dados apos o fim do contrato?
5. O que preciso fazer se ocorrer vazamento de dados pessoais?
