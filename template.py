EMAIL_SIGNATURE_TEMPLATE = """
<div dir="ltr">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"
         style="border-collapse:collapse;border:none !important;
                mso-table-lspace:0pt;mso-table-rspace:0pt;
                font-family:Arial, sans-serif;font-size:12px;color:#000000;">
    <tr>
      <!-- Stacked Logos -->
      <td valign="top"
          style="padding:4px 6px 2px 0;
                 width:170px;min-width:170px;
                 border:none !important;">
        {logos_block}
      </td>

      <!-- Divider -->
      <td valign="top"
          style="width:1px;min-width:1px;padding:0;border:none !important;background:#BDBDBD;font-size:0;line-height:0;">
        &nbsp;
      </td>

      <!-- Dynamic Text Block -->
      <td valign="top"
          style="padding:2px 0 2px 20px;border:none !important;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0"
               style="border-collapse:collapse;border:none !important;
                      mso-table-lspace:0pt;mso-table-rspace:0pt;
                      font-family:Arial, sans-serif;color:#000000;
                      line-height:1.35;">

          {details_rows}

        </table>
      </td>
    </tr>
  </table>
</div>
"""
