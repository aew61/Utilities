# this is the required version of CMake necessary
# to run. CMake will fail if you have anything
# less than 3.3
cmake_minimum_required( VERSION 3.3 )

# when CMake generates Makefiles, this setting
# will allow them to print to the console.
set( CMAKE_VERBOSE_MAKEFILE "ON" )

# this points to the root of the cmake directory
# which contains all the toolchains and modules
get_filename_component( CMAKE_LOCAL_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../cmake ABSOLUTE )

# add our custom module path to the CMAKE_MODULE_PATH
# this allows us to say include( <module_name> )
# if <module_name> is located in ${CMAKE_LOCAL_ROOT}/modules
list( APPEND CMAKE_MODULE_PATH ${CMAKE_LOCAL_ROOT}/modules )

# this is the project name and type
project( Utilities CXX )

get_filename_component( SRC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../cpp ABSOLUTE )

# this is where all build intermediate files will go
get_filename_component( OUT_ROOT ${CMAKE_CURRENT_BINARY_DIR}/out ABSOLUTE )

option( RUN_UNIT_TESTS "Unit test support (default OFF)" OFF )
option( RUN_CPP_CHECK  "Static analysis support (default OFF)" OFF )

# documentation variables...ignore for now
set(DOC_PUBLIC_INPUT_LIST )
set(DOC_PRIVATE_INPUT_LIST )

# these variables are set through the python build scripts.
# they are what controls the project build flow.

if( BUILD_UTILITIES )
    # Async library
    add_subdirectory( ${SRC_ROOT}/src/Utilities
                      ${OUT_ROOT}/Utilities )

    # give other subprojects a chance to search for libraries and header
    # files created before the "make install"
    list( APPEND CMAKE_INCLUDE_PATH "${OUT_ROOT}/Utilities" )
    list( APPEND CMAKE_LIBRARY_PATH "${OUT_ROOT}/Utilities" )
endif()

# this variable is also set through the python build scripts.
if( RUN_UNIT_TESTS )

    if( BUILD_UTILITIES )
        # Async unit tests
        add_subdirectory( ${SRC_ROOT}/unitTest/Utilities
                          ${OUT_ROOT}/UtilitiesUnit )
    endif()

endif()


# if( RUN_CPP_CHECK )
#     find_package( cppcheck REQUIRED)
#     if( CPPCHECK_FOUND )
#          # include the .cmake file for CppCheck to run
#          # if( ${CMAKE_SYSTEM_NAME} MATCHES "Windows" )
#               # add windows.cfg (set ( CPPCHECK_LIBRARY_USE "--library=windows.cfg"))
#          # use linux version
#
#        add_custom_target(TARGET
#            # cppcheck target name
#            PRE_BUILD
#            COMMAND ${CMAKE_COMMAND} -E make_directory # output directory
#        )
#     else()
#         message(ERROR "CppCheck not found")
#     endif()
# endif
