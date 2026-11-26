def html_body(date_formatted: str, files: int) -> str:
   html = """\
      <!DOCTYPE html>
      <html lang="pt-BR">
      <head>
      <meta charset="UTF-8">
      </head>
      <body style="margin: 0; padding: 24px 12px; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f1f5f9;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; background-color: #111827; border-radius: 12px; overflow: hidden; border: 1px solid #1f2937;">
         
         <!-- Cabeçalho com Gradiente -->
         <tr>
            <td style="padding: 32px 24px; text-align: center; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);">
            <div style="font-size: 36px; line-height: 1; margin-bottom: 12px;">🚀</div>
            <h1 style="margin: 0; font-size: 22px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; text-transform: uppercase;">
               Drop de Conteúdo Liberado
            </h1>
            </td>
         </tr>

         <!-- Bloco Central -->
         <tr>
            <td style="padding: 32px 24px;">
            <p style="margin: 0 0 20px 0; font-size: 15px; line-height: 1.6; color: #cbd5e1;">
               Fala, comunidade! Os materiais da gravação de hoje já foram finalizados, auditados e empacotados com sucesso.
            </p>

            <!-- Card de Métricas -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0b0f19; border: 1px solid #1f2937; border-radius: 8px; margin-bottom: 24px;">
               <tr>
                  <td style="padding: 16px; text-align: center; border-right: 1px solid #1f2937; width: 50%;">
                  <span style="display: block; font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Data do Drop</span>
                  <strong style="font-size: 15px; color: #38bdf8;">{data_drop}</strong>
                  </td>
                  <td style="padding: 16px; text-align: center; width: 50%;">
                  <span style="display: block; font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;">Arquivos Inclusos</span>
                  <strong style="font-size: 15px; color: #4ade80;">{total_arquivos} itens</strong>
                  </td>
               </tr>
            </table>

            <!-- Mensagem de Fechamento -->
            <p style="margin: 0 0 12px 0; font-size: 14px; line-height: 1.6; color: #94a3b8;">
               O pacote completo com áudios, artes e anotações segue <strong>em anexo a este e-mail</strong> no formato compactado (<code>.zip</code>).
            </p>
            <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #cbd5e1;">
               Obrigado por apoiar a produção independente de conteúdo! 🔥
            </p>
            </td>
         </tr>

         <!-- Rodapé -->
         <tr>
            <td style="padding: 16px 24px; background-color: #080c14; text-align: center; border-top: 1px solid #1f2937;">
            <span style="font-size: 12px; color: #64748b;">
               Bot Automático de Distribuição • VIP Creator Feed
            </span>
            </td>
         </tr>
      </table>
      </body>
      </html>
   """

   # return html.format(
   #    data_drop=date_formatted,
   #    total_arquivos=len(allowed_files)
   # )

   return html.replace('{data_drop}', date_formatted).replace(
      '{total_arquivos}', str(files)
   )