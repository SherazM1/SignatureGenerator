EMAIL_SIGNATURE_TEMPLATE = """
<div dir="ltr">
  <table cellpadding="0" cellspacing="0" border="0"
         style="border-collapse:collapse;border:none;
                mso-table-lspace:0pt;mso-table-rspace:0pt;
                font-family:Arial, sans-serif;font-size:12px;color:#000000;">
    <tr>
      <!-- Logo -->
      <td valign="middle"
          style="padding:8px 18px 8px 0;
                 border:none;
                 border-right:1px solid #BDBDBD;">
        <a href="{company_website}" target="_blank"
           style="text-decoration:none;display:block;">
          <img src="{logo_url}" alt="logo"
               style="display:block;height:80px;width:auto;border:0;outline:none;text-decoration:none;">
        </a>
      </td>

      <!-- Text -->
      <td valign="middle"
          style="padding:8px 0 8px 18px;border:none;">
        <table cellpadding="0" cellspacing="0" border="0"
               style="border-collapse:collapse;border:none;
                      mso-table-lspace:0pt;mso-table-rspace:0pt;
                      font-family:Arial, sans-serif;color:#000000;line-height:1.35;">

          <!-- Name -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <span style="font-size:14px;font-weight:bold;color:#000000;">
                {name}
              </span>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <span style="font-size:12px;font-weight:bold;color:#000000;">
                {title}
              </span>
            </td>
          </tr>

          <!-- Phone -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <a href="tel:{phone}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {phone}
              </a>
            </td>
          </tr>

          <!-- Email -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <a href="mailto:{email}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {email}
              </a>
            </td>
          </tr>

          <!-- Website 1 -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <a href="{website_1_url}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {website_1}
              </a>
            </td>
          </tr>

          <!-- Website 2 (optional) -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <a href="{website_2_url}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {website_2}
              </a>
            </td>
          </tr>

          <!-- Address line 1 -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <span style="font-size:12px;color:#000000;">
                {address_line_1}
              </span>
            </td>
          </tr>

          <!-- Address line 2 (optional) -->
          <tr>
            <td style="padding-bottom:6px;border:none;">
              <span style="font-size:12px;color:#000000;">
                {address_line_2}
              </span>
            </td>
          </tr>

          <!-- Optional extra line -->
          <tr>
            <td style="padding-bottom:0;border:none;">
              <span style="font-size:11px;color:#000000;">
                {social_line}
              </span>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</div>
"""
