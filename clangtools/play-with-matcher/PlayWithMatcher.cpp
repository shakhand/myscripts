#include <string>

#include "clang/AST/AST.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang/Basic/SourceManager.h"
#include "clang/Frontend/TextDiagnosticPrinter.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Refactoring.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/raw_ostream.h"

using namespace clang;
using namespace clang::ast_matchers;
using namespace clang::driver;
using namespace clang::tooling;

static llvm::cl::OptionCategory ToolingSampleCategory("Matcher Sample");

class IfStmtHandler : public MatchFinder::MatchCallback {
public:
  IfStmtHandler(Replacements *Replace) : Replace(Replace) {}

  virtual void run(const MatchFinder::MatchResult &Result) {
    // The matched 'if' statement was bound to 'ifStmt'.
    if (const IfStmt *IfS = Result.Nodes.getNodeAs<clang::IfStmt>("ifStmt")) {
      const Stmt *Then = IfS->getThen();
      Replacement Rep(*(Result.SourceManager), Then->getLocStart(), 0,
                      "// the 'if' part\n");
      Replace->insert(Rep);

      if (const Stmt *Else = IfS->getElse()) {
        Replacement Rep(*(Result.SourceManager), Else->getLocStart(), 0,
                        "// the 'else' part\n");
        Replace->insert(Rep);
      }
    }
  }

private:
  Replacements *Replace;
};

class CxxRecordDeclHandler : public MatchFinder::MatchCallback
{
public:
  CxxRecordDeclHandler(Replacements* replacement) : mReplacement(replacement){}

  virtual void run(const MatchFinder::MatchResult &Result) {
    if (const CXXRecordDecl *classDecl = 
            Result.Nodes.getNodeAs<clang::CXXRecordDecl>("testClassDecl")) {

      for(auto b = classDecl->method_begin(), e = classDecl->method_end(); b != e; ++b )
      {
       
        if( b->getAccess() == AS_public )

          llvm::outs() << "name:" << b->getNameInfo().getAsString() 
                       << " start pos: " << b->getLocStart().printToString(*Result.SourceManager)
                       << " end pos: " << b->getLocEnd().printToString(*Result.SourceManager) <<"\n";


            Replacement Rep(*(Result.SourceManager), b->getLocStart(), 0,
                      "// public method\n");
            mReplacement->insert(Rep);


      }
    }
    //   const Stmt *Then = IfS->getThen();


    //   if (const Stmt *Else = IfS->getElse()) {
    //     Replacement Rep(*(Result.SourceManager), Else->getLocStart(), 0,
    //                     "// the 'else' part\n");
    //     Replace->insert(Rep);
    // }
    }

  private:
    Replacements *mReplacement;
  
};

int main(int argc, const char **argv) {
  CommonOptionsParser op(argc, argv, ToolingSampleCategory);
  RefactoringTool Tool(op.getCompilations(), op.getSourcePathList());

  // Set up AST matcher callbacks.
  IfStmtHandler HandlerForIf(&Tool.getReplacements());
  CxxRecordDeclHandler cxxRecordDeclHandler(&Tool.getReplacements());

  MatchFinder Finder;
  Finder.addMatcher(ifStmt().bind("ifStmt"), &HandlerForIf);

  Finder.addMatcher(cxxRecordDecl(isDerivedFrom(cxxRecordDecl())).bind("testClassDecl"), &cxxRecordDeclHandler);
  // Run the tool and collect a list of replacements. We could call runAndSave,
  // which would destructively overwrite the files with their new contents.
  // However, for demonstration purposes it's interesting to show the
  // replacements.
  if (int Result = Tool.run(newFrontendActionFactory(&Finder).get())) {
    return Result;
  }

  llvm::outs() << "Replacements collected by the tool:\n";
  for (auto &r : Tool.getReplacements()) {
    llvm::outs() << r.toString() << "\n";
  }

  return 0;
}