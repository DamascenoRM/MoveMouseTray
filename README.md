# MoveMouseTray

MoveMouseTray é um utilitário avançado para Windows que simula a atividade do mouse para impedir que softwares de monitoramento de presença, como o Microsoft Teams, identifiquem a ausência do usuário. O programa movimenta o mouse periodicamente após um período de inatividade, garantindo que o sistema não entre em estado de repouso ou sinalize ausência.

## Funcionalidades

- **Detecção de Inatividade:** Monitora a atividade do mouse e do teclado para detectar quando o usuário está inativo.
- **Movimentação Automática do Mouse:** Movimenta o mouse automaticamente após um período de inatividade configurável.
- **Controle via Bandeja do Sistema:** Oferece um ícone na bandeja do sistema que permite iniciar, pausar e fechar o programa facilmente.
- **Configurador:** Permite ajustar as configurações de tempo de inatividade, intervalo entre movimentos, permissões de tela de bloqueio, hibernação e suspensão, ativação de movimento do mouse e movimentos múltiplos do mouse diretamente a partir do menu da bandeja do sistema.
- **Persistência de Configurações:** Salva e carrega configurações automaticamente entre reinicializações.

## Requisitos

- Python 3.6 ou superior

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/DamascenoRM/MoveMouseTray.git
   cd MoveMouseTray
   ```

2. Crie um ambiente virtual e ative-o:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # Para Windows
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

4. Empacote o aplicativo usando PyInstaller:
   ```sh
   pyinstaller MoveMouseTray.spec
   ```

## Uso

1. Execute o arquivo `MoveMouseTray.exe` gerado na pasta `dist`.

2. Um ícone aparecerá na bandeja do sistema. Clique com o botão direito no ícone para acessar o menu:
   - **Start:** Inicia o monitoramento de inatividade e a movimentação do mouse.
   - **Stop:** Pausa a movimentação do mouse.
   - **Configurador:** Abre a janela de configurações para ajustar os parâmetros do programa.
   - **Quit:** Fecha o programa.

## Configurador

O configurador permite ajustar as seguintes opções:
- **Tempo de Inatividade:** Tempo em segundos antes de o mouse começar a se mover após detectar inatividade.
- **Intervalo entre Movimentos:** Intervalo em segundos entre cada movimento do mouse.
- **Permitir Tela de Bloqueio:** Ativar ou desativar a permissão para o sistema bloquear a tela.
- **Permitir Hibernação:** Ativar ou desativar a permissão para o sistema hibernar.
- **Permitir Suspensão:** Ativar ou desativar a permissão para o sistema entrar em suspensão.
- **Ativar Movimento do Mouse:** Ativar ou desativar o movimento automático do mouse.
- **Ativar Movimentos Múltiplos:** Ativar ou desativar múltiplos movimentos do mouse.
- **Quantidade de Movimentos Múltiplos:** Número de movimentos múltiplos do mouse.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para relatar bugs ou solicitar novas funcionalidades. Para contribuições de código, faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Aviso Legal

Este software é fornecido "como está", sem garantia de qualquer tipo, expressa ou implícita. O uso deste software é de sua inteira responsabilidade.

---

### Recursos Adicionais

- [Documentação Oficial do PyAutoGUI](https://pyautogui.readthedocs.io/)
- [Documentação Oficial do Pynput](https://pynput.readthedocs.io/en/latest/)
- [Documentação Oficial do Pystray](https://pystray.readthedocs.io/en/latest/)
- [Documentação Oficial do Pillow](https://pillow.readthedocs.io/en/stable/)
