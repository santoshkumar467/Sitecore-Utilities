<%@ Import Namespace="System" %>
<%@ Import Namespace="System.Web.Security" %>
<%@ Import Namespace="Sitecore.Security.Accounts" %>
<%@ Page Language="C#" Debug="true" %>
<HTML>
   <script runat="server" language="C#">
   	string log = string.Empty;
   	string userName = "sitecore\\admin";
	public void Page_Load(object sender, EventArgs e)
	{
		
		var action = Request["action"];
		Sitecore.Diagnostics.Log.Info("Reset admin password action call: " +action, this);
		if (action == "resetPassword" )
		{
			try {
				var user = Membership.GetUser(userName);
				user.UnlockUser();
				user.ChangePassword(user.ResetPassword(), "Password@1234");

			} catch (MembershipCreateUserException ex) 
			{
				log += string.Format("user: {0} : {1}<br>\n",userName,ex.Message);
			}

			if (string.IsNullOrEmpty(log)) { log = "Password reset was successful."; }
		}
	}
   </script>
   <body>
   <h1>Reset Sitecore Admin Password:</h1>
   
   	<h2><a href="?action=resetPassword">Reset password</a></h2>
   	
	<h3>
      <%=log %>
   </h3>
   </body>
</HTML>