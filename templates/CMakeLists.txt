set(prefix %%PROBLEM_NAME%%)

add_executable(${prefix}_main main.cpp main.h)

cxx_test(${prefix}_tests tests.cpp)
target_link_libraries(${prefix}_tests ${Boost_LIBRARIES})

add_custom_command(OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/out.cpp
        COMMAND caide-inliner -t ${CMAKE_CURRENT_BINARY_DIR} -s ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
        -o ${CMAKE_CURRENT_SOURCE_DIR}/out.cpp
        -- ${CLANG_INLINER_FLAGS} -I ${CMAKE_CURRENT_SOURCE_DIR}
        IMPLICIT_DEPENDS CXX ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp)

set_source_files_properties(out.cpp PROPERTIES GENERATED TRUE)
add_executable(${prefix}_out out.cpp)