{
  gEnv->SetValue("Root.PluginPath", "@PWD@/etc/plugins");
  gSystem->AddIncludePath("@PWD@/include");
  gSystem->AddIncludePath("@PWD@/cint/cint/include");
  gSystem->AddIncludePath("@PWD@/cint/cint/stl");
  gROOT->GetPluginManager()->LoadHandlersFromPluginDirs("");
  gROOT->GetPluginManager()->AddHandler("TVirtualPS","image",
					"TImageDump","Postscript",
					"TImageDump()");
  gROOT->GetPluginManager()->AddHandler("TVirtualStreamerInfo",
					"*","TStreamerInfo",
					"RIO","TStreamerInfo()");
  gROOT->GetPluginManager()->AddHandler("TVirtualGraphPainter", "*",
					"TGraphPainter","GraphPainter",
					"TGraphPainter()");
  THtml html;
  html.SetProductName("ROOT");
  html.SetEtcDir("@PWD@/etc/html");
  html.SetHomepage("http://root.cern.ch");
  html.LoadAllLibs();
  html.SetBatch(kTRUE);
  html.MakeAll();
}
