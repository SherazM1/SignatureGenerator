EMAIL_SIGNATURE_TEMPLATE = """
<div dir="ltr">
  <table cellpadding="0" cellspacing="0" border="0"
         style="border-collapse:collapse;font-family:Arial, sans-serif;font-size:12px;color:#000000;">
    <tr>
      <!-- Logo -->
      <td valign="middle"
          style="padding:8px 18px 8px 0;border-right:1px solid #BDBDBD;">
        <a href="{company_website}" target="_blank"
           style="text-decoration:none;display:block;">
          <img src="{logo_url}" alt="logo"
               style="display:block;height:80px;width:auto;border:0;">
        </a>
      </td>

      <!-- Text -->
      <td valign="middle" style="padding:8px 0 8px 18px;">
        <table cellpadding="0" cellspacing="0" border="0"
               style="border-collapse:collapse;font-family:Arial, sans-serif;
                      color:#000000;line-height:1.35;">

          <!-- Name -->
          <tr>
            <td style="padding-bottom:6px;">
              <span style="font-size:14px;font-weight:bold;color:#000000;">
                {name}
              </span>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td style="padding-bottom:6px;">
              <span style="font-size:12px;font-weight:bold;color:#000000;">
                {title}
              </span>
            </td>
          </tr>

          <!-- Phone -->
          <tr>
            <td style="padding-bottom:6px;">
              <a href="tel:{phone}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {phone}
              </a>
            </td>
          </tr>

          <!-- Email -->
          <tr>
            <td style="padding-bottom:6px;">
              <a href="mailto:{email}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {email}
              </a>
            </td>
          </tr>

          <!-- Website -->
          <tr>
            <td style="padding-bottom:6px;">
              <a href="{website_1_url}"
                 style="font-size:12px;color:#000000;text-decoration:none;">
                {website_1}
              </a>
            </td>
          </tr>

          <!-- Address -->
          <tr>
            <td style="padding-bottom:6px;">
              <span style="font-size:12px;color:#000000;">
                {address_line_1}
              </span>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</div>
"""
