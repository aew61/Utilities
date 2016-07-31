# this is the required version of CMake necessary
# to run. CMake will fail if you have anything
# less than 3.3
cmake_minimum_required( VERSION 3.3 )

# when CMake generates Makefiles, this setting
# will allow them to print to the console.
set( CMAKE_VERBOSE_MAKEFILE "ON" )

# this points to the root of the cmake directory
# which contains all the toolchains and modules
get_filename_component( CMAKE_LOCAL_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/cmake ABSOLUTE )

get_filename_component( CMAKE_GLOBAL_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../build/cmake ABSOLUTE )

list( APPEND CMAKE_MODULE_PATH ${CMAKE_LOCAL_ROOT}/modules )
list( APPEND CMAKE_MODULE_PATH ${CMAKE_GLOBAL_ROOT}/modules )

# Project name
project( Utilities CXX )

# source code root directory
get_filename_component( SRC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/cpp/src ABSOLUTE )

# this is where all build intermediate files will go
get_filename_component( OUT_ROOT ${CMAKE_CURRENT_BINARY_DIR}/out ABSOLUTE )

# Public header file root directory
get_filename_component( INC_ROOT ${SRC_ROOT}/../include ABSOLUTE )

get_filename_component( CONFIG_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../build/out/include ABSOLUTE )

# this is where we could get the Version numbering from Version.h and
# save them as CMake variables. for now, lets just declare them
# set( PROJECT_VERSION_MAJOR "1" )
# set( PROJECT_VERSION_MINOR "0" )
# set( PROJECT_VERSION_PATCH "0" )

# Source files
set( UTILITIES_SRCS
    ${SRC_ROOT}/Semaphore.cc
)

# Public header files (installed together with libraries)
set( UTILITIES_PUBLIC_HEADERS
    ${INC_ROOT}/Utilities/LibraryExport.h
    ${INC_ROOT}/Utilities/Semaphore.h
)

set( UTILITIES_PRIVATE_HEADERS
)

# setup visual studio source groups
source_group( PublicHeaders FILES ${UTILITIES_PUBLIC_HEADERS} )

# Directories to search for header files
set( INCLUDE_DIRS
    ${INC_ROOT}
    ${SRC_ROOT}
    ${CONFIG_ROOT}
    ${CMAKE_PREFIX_PATH}/include
)

set( UTILITIES_COMPILE_DEFINITIONS )

# check required libraries and header files and such.
# this will fail CMake if set to False due to required
# modules requiring their own dependencies
set( DEPENDENCY_CHECK FALSE )

include( GNUInstallDirs )

# set( ${PROJECT_NAME}_IMPORTED_LIST
#     # all libraries to import when building Async
# )
# include(ProjectLinker)

# if( NOT DEPENDENCY_CHECK )
#     message( SEND_ERROR "Required header files or libraries not found" )
# endif()

include_directories( ${INCLUDE_DIRS} )

# Logging library
set( UTILITIES_LIB_NAME ${PROJECT_NAME} )

# Shared Library export header file supporte
include( GenerateExportHeader )

add_library( ${UTILITIES_LIB_NAME} SHARED ${UTILITIES_SRCS} ${UTILITIES_PUBLIC_HEADERS} ${UTILITIES_PRIVATE_HEADERS})
# if( ${${PROJECT_NAME}_IMPORTED_LIBS_LENGTH} GREATER 0 )
#     target_link_libraries( ${ASYNC_LIB_NAME} ${${PROJECT_NAME}_IMPORTED_LIBS} )
# endif()

set_target_properties( ${UTILITIES_LIB_NAME} PROPERTIES
    PUBLIC_HEADER       "${UTILITIES_PUBLIC_HEADERS}"
    COMPILE_DEFINITIONS "${UTILITIES_COMPILE_DEFINITIONS}"
    SOVERSION           "${PROJECT_VERSION_MAJOR}"
    VERSION             "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}"
)

# install targets
install( TARGETS ${UTILITIES_LIB_NAME}
         RUNTIME        DESTINATION ${CMAKE_INSTALL_BINDIR}
         LIBRARY        DESTINATION ${CMAKE_INSTALL_LIBDIR}
         ARCHIVE        DESTINATION ${CMAKE_INSTALL_LIBDIR}
         PUBLIC_HEADER  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/Utilities
)

if( MSVC )
    get_filename_component( PDB_DIR ${CMAKE_PREFIX_PATH}/../../${CMAKE_RUNTIME_OUTPUT_DIRECTORY} ABSOLUTE )
    install( FILES ${PDB_DIR}/${PROJECT_NAME}.pdb
        DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

if( RUN_UNIT_TESTS )

    get_filename_component( TEST_SRC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/cpp/unitTest/src ABSOLUTE )
    get_filename_component( TEST_INC_ROOT ${TEST_SRC_ROOT}/../include ABSOLUTE )

     enable_testing()
    
    list( APPEND CMAKE_FIND_ROOT_PATH ${INSTALL_ROOT} )

    set( ${PROJECT_NAME}_IMPORTED_LIST
        # all libraries to import when building Async
        "gtest"
    )
    include(ProjectLinker)

    if( ${${PROJECT_NAME}_IMPORTED_LIBS_LENGTH} GREATER 0 )

        # source files
        set( UTILITIES_UNIT_SOURCES

            # Utilities sources
            # ${SRC_ROOT}/Semaphore.cc

            # AsyncUnitTests sources
            ${TEST_SRC_ROOT}/Semaphore_unit.cc
            ${TEST_SRC_ROOT}/main.cc
        )

        set( UTILITIES_UNIT_HEADERS
        )

        # directories to search for header files
        set( INCLUDE_DIRS
            ${INC_ROOT}
            ${TEST_INC_ROOT}
            ${CONFIG_ROOT}
            ${${PROJECT_NAME}_INCLUDES} # the list of include dirs found by ProjectLinker
        )

        if( MSVC )
            include( GNUInstallDirs )
        elseif( ${CMAKE_SYSTEM_NAME} MATCHES "Linux" )
            include( GNUInstallDirs )
            set(TARGET_PTHREADS_LIB "pthread" )

            # this process would work, just in doing so would make it hard
            # to import binaries and run them like with FT and RT projects.
            # set( TARGET_GCOV_LIB "gcov" )
        elseif( APPLE )
            include( GNUInstallDirs )
            set(TARGET_PTHREADS_LIB "pthread")
        else()
            message(SEND_ERROR "OS [${CMAKE_SYSTEM_NAME}] not supported")
        endif()

        # add_definitions(-DUTILITIES_STATIC_DEFINE) #

        include_directories( ${INCLUDE_DIRS} )

        add_executable( ${PROJECT_NAME}_Unit ${UTILITIES_UNIT_SOURCES} ${UTILITIES_UNIT_HEADERS} )
        if( ${${PROJECT_NAME}_IMPORTED_LIBS_LENGTH} GREATER 0 )
            target_link_libraries( ${PROJECT_NAME}_Unit ${${PROJECT_NAME}_IMPORTED_LIBS} )
        endif()

        string( TOLOWER "${CMAKE_BUILD_TYPE}" CMAKE_BUILD_TYPE_LOWER )
        if( CMAKE_BUILD_TYPE_LOWER STREQUAL "debug" )
            message( "Linking executable for Debug" )
            target_link_libraries( ${PROJECT_NAME}_Unit
                ${PROJECT_NAME}
                ${TARGET_PTHREADS_LIB}
            #     ${TARGET_GCOV_LIB}
            )
            # if( ENABLE_COVERAGE AND ${CMAKE_SYSTEM_NAME} MATCHES "Linux" )
            #     message("LINKING UTILITIES WITH GCOV")
            #     message("CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")
            #     target_link_libraries( ${PROJECT_NAME}
            #         ${TARGET_GCOV_LIB}
            #     )
            # endif()
        else()
            message( "Linking executable for Release" )
            target_link_libraries( ${PROJECT_NAME}_Unit
                ${PROJECT_NAME}
                ${TARGET_PTHREADS_LIB}
            )
        endif()

    else()
        message( WARNING "Gtest Framework not found...skipping unit tests")
    endif()
endif()
