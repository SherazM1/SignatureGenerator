EMAIL_SIGNATURE_TEMPLATE = """
<div dir="ltr">
  <table cellpadding="0" cellspacing="0" border="0"
         style="border-collapse:collapse;font-family:Arial, sans-serif;font-size:12px;color:#555555;">
    <tr>
      <!-- Logo cell -->
      <td valign="top" style="padding:0 16px 0 0;border-right:1px solid #BDBDBD;">
        <a href="{company_website}" target="_blank" rel="nofollow noreferrer"
           style="text-decoration:none;display:block;">
          <img src="{logo_url}" alt="logo" border="0"
               style="display:block;height:60px;width:auto;">
        </a>
      </td>

      <!-- Text cell -->
      <td valign="top" style="padding:0 0 0 16px;">
        <table cellpadding="0" cellspacing="0" border="0"
               style="border-collapse:collapse;font-family:Arial, sans-serif;">

          <!-- Name -->
          <tr>
            <td style="padding-bottom:2px;">
              <span style="font-size:13px;font-weight:bold;color:#0062B8;">
                {name}
              </span>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td style="padding-bottom:8px;">
              <span style="font-size:11px;font-weight:bold;color:#666666;">
                {title}
              </span>
            </td>
          </tr>

          <!-- Phone -->
          <tr>
            <td style="padding-bottom:2px;">
              <a href="tel:{phone}"
                 style="font-size:12px;color:#0062B8;text-decoration:underline;">
                {phone}
              </a>
            </td>
          </tr>

          <!-- Email -->
          <tr>
            <td style="padding-bottom:2px;">
              <a href="mailto:{email}"
                 style="font-size:12px;color:#0062B8;text-decoration:underline;">
                {email}
              </a>
            </td>
          </tr>

          <!-- Website 1 -->
          <tr>
            <td style="padding-bottom:2px;">
              <a href="{website_1_url}"
                 style="font-size:12px;color:#0062B8;text-decoration:underline;">
                {website_1}
              </a>
            </td>
          </tr>

          <!-- Website 2 -->
          <tr>
            <td style="padding-bottom:2px;">
              <a href="{website_2_url}"
                 style="font-size:12px;color:#0062B8;text-decoration:underline;">
                {website_2}
              </a>
            </td>
          </tr>

          <!-- Address line 1 -->
          <tr>
            <td style="padding-bottom:2px;">
              <span style="font-size:12px;color:#555555;">
                {address_line_1}
              </span>
            </td>
          </tr>

          <!-- Address line 2 -->
          <tr>
            <td style="padding-bottom:8px;">
              <span style="font-size:12px;color:#555555;">
                {address_line_2}
              </span>
            </td>
          </tr>

          <!-- Optional social / extra text (no images, keeps one-image rule) -->
          <tr>
            <td>
              <span style="font-size:11px;color:#555555;">
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
