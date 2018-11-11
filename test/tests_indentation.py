import unittest
import yattag
from yattag import indent


class TestIndent(unittest.TestCase):

    def setUp(self):
    
        self.maxDiff = None
    
        self.targets = {
            '<p>aaa</p>': '<p>aaa</p>',
            '<html><body><p>1</p><p>2</p></body></html>': """\
<html>
    <body>
        <p>1</p>
        <p>2</p>
    </body>
</html>""",
            '<body><div id="main"><img src="photo1"><img src="photo2"></div></body>': """\
<body>
    <div id="main">
        <img src="photo1">
        <img src="photo2">
    </div>
</body>""",
            """
            <html>
            <body>
            <p><strong>Important:</strong> the content of nodes that directly contain text should be preserved.</p>
            <div>
            <p>But the content of nodes that don't (like the parent div here) should be indented.</p>
            </div>
            </body>
            </html>
""": """\
<html>
    <body>
        <p><strong>Important:</strong> the content of nodes that directly contain text should be preserved.</p>
        <div>
            <p>But the content of nodes that don't (like the parent div here) should be indented.</p>
        </div>
    </body>
</html>""",
            '<p>Hello <i>world</i>!</p>': "<p>Hello <i>world</i>!</p>",
            
            '<?xml version="1.0" encoding="utf-8"?><a><b/><b/></a>': '''\
<?xml version="1.0" encoding="utf-8"?>
<a>
    <b/>
    <b/>
</a>''',
    """\
<test_processing_instruction>
<?xml-stylesheet type="text/css" href="..\..\..\..\..\..\..\SharedResourceFiles\MAIN\Stylesheets\CSS\dita_branded_preview.css" title="Branded New"?>
<?without_content?>
</test_processing_instruction>""":
"""\
<test_processing_instruction>
    <?xml-stylesheet type="text/css" href="..\..\..\..\..\..\..\SharedResourceFiles\MAIN\Stylesheets\CSS\dita_branded_preview.css" title="Branded New"?>
    <?without_content?>
</test_processing_instruction>"""
        }
        
        self.targets_indent_text = { '<p>Hello <i>world</i>!</p>': """\
<p>
    Hello 
    <i>
        world
    </i>
    !
</p>"""
        }
        
        self.source_code = """\
<body><code>\
package com.google.android.gms.auth.api.signin.internal;

import android.os.Parcel;
import android.os.Parcelable.Creator;
import android.text.TextUtils;
import com.google.android.gms.auth.api.signin.EmailSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.internal.safeparcel.SafeParcelable;
import com.google.android.gms.common.internal.zzx;
import org.json.JSONObject;

public final class SignInConfiguration implements SafeParcelable {
    public static final Creator&lt;SignInConfiguration&gt; CREATOR = new zzp();
    final int versionCode;
    private final String zzXL;
    private EmailSignInOptions zzXM;
    private GoogleSignInOptions zzXN;
    private String zzXO;
    private String zzXd;

    SignInConfiguration(int versionCode, String consumerPkgName, String serverClientId, EmailSignInOptions emailConfig, GoogleSignInOptions googleConfig, String apiKey) {
        this.versionCode = versionCode;
        this.zzXL = zzx.zzcM(consumerPkgName);
        this.zzXd = serverClientId;
        this.zzXM = emailConfig;
        this.zzXN = googleConfig;
        this.zzXO = apiKey;
    }

    public SignInConfiguration(String consumerPkgName) {
        this(2, consumerPkgName, null, null, null, null);
    }</code></body>
"""

        self.source_code_target = """\
<body>
    <code>
        package com.google.android.gms.auth.api.signin.internal;
        
        import android.os.Parcel;
        import android.os.Parcelable.Creator;
        import android.text.TextUtils;
        import com.google.android.gms.auth.api.signin.EmailSignInOptions;
        import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
        import com.google.android.gms.common.internal.safeparcel.SafeParcelable;
        import com.google.android.gms.common.internal.zzx;
        import org.json.JSONObject;
        
        public final class SignInConfiguration implements SafeParcelable {
            public static final Creator&lt;SignInConfiguration&gt; CREATOR = new zzp();
            final int versionCode;
            private final String zzXL;
            private EmailSignInOptions zzXM;
            private GoogleSignInOptions zzXN;
            private String zzXO;
            private String zzXd;
        
            SignInConfiguration(int versionCode, String consumerPkgName, String serverClientId, EmailSignInOptions emailConfig, GoogleSignInOptions googleConfig, String apiKey) {
                this.versionCode = versionCode;
                this.zzXL = zzx.zzcM(consumerPkgName);
                this.zzXd = serverClientId;
                this.zzXM = emailConfig;
                this.zzXN = googleConfig;
                this.zzXO = apiKey;
            }
        
            public SignInConfiguration(String consumerPkgName) {
                this(2, consumerPkgName, null, null, null, null);
            }
    </code>
</body>"""
        


    def test_indent(self):
        for source, target in self.targets.items():
            self.assertEqual(
                indent(source, indentation = "    "),
                target
            )
        
    def test_idempotent(self):
        for source, target in self.targets.items():
            self.assertEqual(
                indent(source),
                indent(indent(source))
            )
            
    def test_indent_text_option(self):
        for source, target in self.targets_indent_text.items():
            self.assertEqual(
                indent(source, indentation = "    ", indent_text = True),
                target
            )
            
    def test_indent_each_line(self):
        self.assertEqual(
            indent(self.source_code, indentation = "    ", indent_text = yattag.EACH_LINE),
            self.source_code_target
        )
        
                


if __name__ == '__main__':
    unittest.main()
