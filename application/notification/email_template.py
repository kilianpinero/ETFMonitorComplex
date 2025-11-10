class EmailTemplate:
    @staticmethod
    def build(report_rows: list[dict | dict[str, str]]) -> str:
        rows_html = ''
        for row in report_rows:
            style = " style='background-color:#ffeeee;'" if row.get('alert') else ''
            rows_html += (
                f"<tr{style}>"
                f"<td>{row.get('ticker', '')}</td>"
                f"<td>{row.get('drop_percentage', '')}</td>"
                f"<td>{row.get('highest_price', '')}</td>"
                f"<td>{row.get('current_price', '')}</td>"
                f"<td>{'ALERTA' if row.get('alert') else 'Sin alerta'}</td>"
                f"</tr>"
            )
        return f"""
         <html>
           <body>
             <h3>Resumen de caídas y precios ETFs y acciones</h3>
             <table border="1" cellpadding="6" cellspacing="0">
               <tr style='background-color:#f0f0f0;'>
                 <th>Ticker</th>
                 <th>Caída (%)</th>
                 <th>Precio más alto</th>
                 <th>Precio actual</th>
                 <th>Alerta</th>
               </tr>
               {rows_html}
             </table>
             <br>
           </body>
         </html>
         """