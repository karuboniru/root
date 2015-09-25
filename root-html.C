{
  gSystem->AddIncludePath("-I@PWD@/include");
  gSystem->AddIncludePath("-I@PWD@/cint/cint/include");
  gSystem->AddIncludePath("-I@PWD@/cint/cint/stl");
  gSystem->AddIncludePath("-I@PWD@/cint/cint/lib");
  TInterpreter::Instance()->AddIncludePath("@PWD@/include");
  TInterpreter::Instance()->AddIncludePath("@PWD@/cint/cint/include");
  TInterpreter::Instance()->AddIncludePath("@PWD@/cint/cint/stl");
  TInterpreter::Instance()->AddIncludePath("@PWD@/cint/cint/lib");
  #include <RtypesCint.h>
  #include <iostream>
  #include <string>
  #include <DllImport.h>
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
  delete (TFile*) gROOT->ProcessLine(".x tutorials/hsimple.C");
  gSystem->Exec("mv hsimple.root tutorials/hsimple.root");
  THtml html;
  html.SetEtcDir("@PWD@/etc/html");
  html.SetSourceDir(".");
  html.LoadAllLibs();
  html.SetBatch(kTRUE);
  html.MakeAll();
}
