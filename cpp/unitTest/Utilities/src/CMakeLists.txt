# this is the required version of CMake necessary
# to run. CMake will fail if you have anything
# less than 3.3
cmake_minimum_required( VERSION 3.3 )

# when CMake generates Makefiles, this setting
# will allow them to print to the console.
set( CMAKE_VERBOSE_MAKEFILE "ON" )

# this points to the root of the cmake directory
# which contains all the toolchains and modules
get_filename_component( CMAKE_LOCAL_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../../../cmake ABSOLUTE )
get_filename_component( CMAKE_GLOBAL_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../../../build/cmake ABSOLUTE )

list( APPEND CMAKE_MODULE_PATH ${CMAKE_LOCAL_ROOT}/modules )
list( APPEND CMAKE_MODULE_PATH ${CMAKE_GLOBAL_ROOT}/modules )

# Project name
project( Utilities_unit CXX )

# source code root directory
get_filename_component( TEST_SRC_ROOT ${CMAKE_CURRENT_SOURCE_DIR} ABSOLUTE )
get_filename_component( SRC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../../src ABSOLUTE )

# Public header file root directory
get_filename_component( TEST_INC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../include ABSOLUTE )

get_filename_component( INC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../../include ABSOLUTE )

get_filename_component( CONFIG_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../../../build/out/include ABSOLUTE )


if( RUN_UNIT_TESTS )
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
            ${SRC_ROOT}/Utilities/Semaphore.cc

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

        add_definitions(-DUTILITIES_STATIC_DEFINE) #

        include_directories( ${INCLUDE_DIRS} )

        add_executable( ${PROJECT_NAME} ${UTILITIES_UNIT_SOURCES} )
        if( ${${PROJECT_NAME}_IMPORTED_LIBS_LENGTH} GREATER 0 )
            target_link_libraries( ${PROJECT_NAME} ${${PROJECT_NAME}_IMPORTED_LIBS} )
        endif()

        string( TOLOWER "${CMAKE_BUILD_TYPE}" CMAKE_BUILD_TYPE_LOWER )
        if( CMAKE_BUILD_TYPE_LOWER STREQUAL "debug" )
            message( "Linking executable for Debug" )
            target_link_libraries( ${PROJECT_NAME}
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
            target_link_libraries( ${PROJECT_NAME}
                ${TARGET_PTHREADS_LIB}
            )
        endif()

    else()
        message( WARNING "Gtest Framework not found...skipping unit tests")
    endif()

endif()
