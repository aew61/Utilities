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
    find_library( UTILITIES_LIB_IMPL Utilities
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

# make library target
if( NOT TARGET UTILITIES_LIB )
    add_library( UTILITIES_LIB SHARED IMPORTED )

    # will set .so for unix systems and .dll for windows
    set_property( TARGET UTILITIES_LIB PROPERTY
        IMPORTED_LOCATION ${UTILITIES_SHARED_LIB} )

    # need to link to .lib files for windows
    if( ${CMAKE_SYSTEM_NAME} MATCHES "Windows" )
        set_property( TARGET UTILITIES_LIB PROPERTY
            IMPORTED_IMPLIB ${UTILITIES_LIB_IMPL} )
    endif( ${CMAKE_SYSTEM_NAME} MATCHES "Windows" )
endif()

if( UTILITIES_INCLUDES AND UTILITIES_LIB )
    set( UTILITIES_FOUND TRUE )
else()
    set( UTILITIES_FOUND FALSE )
endif()
