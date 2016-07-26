find_path( UTILITIES_INCLUDES Utilities/LibraryExport.h
    HINTS
        ${CMAKE_INSTALL_PREFIX}/include
        ${CMAKE_PREFIX_PATH}/include
)

# find libraries depending on OS.
if( ${CMAKE_SYSTEM_NAME} MATCHES "Windows" )
    # handle dll AND lib?
    find_path( UTILITIES_SHARED_LIB Utilities.dll
        HINTS
            ${CMAKE_INSTALL_PREFIX}/bin
            ${CMAKE_PREFIX_PATH}/bin
    )
    find_library( UTILITIES_LIB Utilities
        HINTS
            ${CMAKE_INSTALL_PREFIX}/lib
            ${CMAKE_PREFIX_PATH}/lib
    )
else()
    find_library( UTILITIES_SHARED_LIB Utilities
        HINTS
            ${CMAKE_INSTALL_PREFIX}/lib
            ${CMAKE_PREFIX_PATH}/lib
    )
endif()

if( NOT UTILITIES_INCLUDES OR NOT UTILITIES_SHARED_LIB )
    set( UTILITIES_FOUND FALSE )
else()
    set( UTILITIES_FOUND TRUE )
endif()
