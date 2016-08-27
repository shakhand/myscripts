set(LLVM_LINK_COMPONENTS support)

add_clang_executable(play-with-matcher
	PlayWithMatcher.cpp
	)

target_link_libraries(play-with-matcher
	clangTooling
	clangBasic
	clangASTMatchers)