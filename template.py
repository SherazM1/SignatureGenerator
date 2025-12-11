EMAIL_SIGNATURE_TEMPLATE = """
<div dir="ltr">
  <table cellpadding="0" cellspacing="0" border="0"
         style="border-collapse:collapse;border:none;
                mso-table-lspace:0pt;mso-table-rspace:0pt;
                font-family:Arial, sans-serif;font-size:12px;color:#000000;">
    <tr>
      <!-- Logo -->
      <td valign="middle"
          style="padding:4px 18px 4px 0;
                 border:none;
                 border-right:1px solid #BDBDBD;">
        <a href="{company_website}" target="_blank"
           style="text-decoration:none;display:block;">
          <img src="{logo_url}" alt="logo"
               style="display:block;height:80px;width:auto;border:0;outline:none;text-decoration:none;">
        </a>
      </td>

      <!-- Dynamic Text Block -->
      <td valign="middle"
          style="padding:4px 0 4px 18px;border:none;">
        <table cellpadding="0" cellspacing="0" border="0"
               style="border-collapse:collapse;border:none;
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
