/****************************************************************************
** Meta object code from reading C++ file 'VehicleStateModel.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../../src/VehicleStateModel.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'VehicleStateModel.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_VehicleStateModel_t {
    QByteArrayData data[12];
    char stringdata0[156];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_VehicleStateModel_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_VehicleStateModel_t qt_meta_stringdata_VehicleStateModel = {
    {
QT_MOC_LITERAL(0, 0, 17), // "VehicleStateModel"
QT_MOC_LITERAL(1, 18, 19), // "vehicleSpeedChanged"
QT_MOC_LITERAL(2, 38, 0), // ""
QT_MOC_LITERAL(3, 39, 15), // "doorOpenChanged"
QT_MOC_LITERAL(4, 55, 18), // "temperatureChanged"
QT_MOC_LITERAL(5, 74, 17), // "mediaStateChanged"
QT_MOC_LITERAL(6, 92, 14), // "updateFromJson"
QT_MOC_LITERAL(7, 107, 3), // "obj"
QT_MOC_LITERAL(8, 111, 12), // "vehicleSpeed"
QT_MOC_LITERAL(9, 124, 8), // "doorOpen"
QT_MOC_LITERAL(10, 133, 11), // "temperature"
QT_MOC_LITERAL(11, 145, 10) // "mediaState"

    },
    "VehicleStateModel\0vehicleSpeedChanged\0"
    "\0doorOpenChanged\0temperatureChanged\0"
    "mediaStateChanged\0updateFromJson\0obj\0"
    "vehicleSpeed\0doorOpen\0temperature\0"
    "mediaState"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_VehicleStateModel[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       5,   14, // methods
       4,   46, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   39,    2, 0x06 /* Public */,
       3,    0,   40,    2, 0x06 /* Public */,
       4,    0,   41,    2, 0x06 /* Public */,
       5,    0,   42,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       6,    1,   43,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::QJsonObject,    7,

 // properties: name, type, flags
       8, QMetaType::Double, 0x00495001,
       9, QMetaType::Bool, 0x00495001,
      10, QMetaType::Double, 0x00495001,
      11, QMetaType::QString, 0x00495001,

 // properties: notify_signal_id
       0,
       1,
       2,
       3,

       0        // eod
};

void VehicleStateModel::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<VehicleStateModel *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->vehicleSpeedChanged(); break;
        case 1: _t->doorOpenChanged(); break;
        case 2: _t->temperatureChanged(); break;
        case 3: _t->mediaStateChanged(); break;
        case 4: _t->updateFromJson((*reinterpret_cast< const QJsonObject(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (VehicleStateModel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&VehicleStateModel::vehicleSpeedChanged)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (VehicleStateModel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&VehicleStateModel::doorOpenChanged)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (VehicleStateModel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&VehicleStateModel::temperatureChanged)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (VehicleStateModel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&VehicleStateModel::mediaStateChanged)) {
                *result = 3;
                return;
            }
        }
    }
#ifndef QT_NO_PROPERTIES
    else if (_c == QMetaObject::ReadProperty) {
        auto *_t = static_cast<VehicleStateModel *>(_o);
        Q_UNUSED(_t)
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< double*>(_v) = _t->vehicleSpeed(); break;
        case 1: *reinterpret_cast< bool*>(_v) = _t->doorOpen(); break;
        case 2: *reinterpret_cast< double*>(_v) = _t->temperature(); break;
        case 3: *reinterpret_cast< QString*>(_v) = _t->mediaState(); break;
        default: break;
        }
    } else if (_c == QMetaObject::WriteProperty) {
    } else if (_c == QMetaObject::ResetProperty) {
    }
#endif // QT_NO_PROPERTIES
}

QT_INIT_METAOBJECT const QMetaObject VehicleStateModel::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_VehicleStateModel.data,
    qt_meta_data_VehicleStateModel,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *VehicleStateModel::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *VehicleStateModel::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_VehicleStateModel.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int VehicleStateModel::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 5)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 5;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 5)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 5;
    }
#ifndef QT_NO_PROPERTIES
    else if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    } else if (_c == QMetaObject::QueryPropertyDesignable) {
        _id -= 4;
    } else if (_c == QMetaObject::QueryPropertyScriptable) {
        _id -= 4;
    } else if (_c == QMetaObject::QueryPropertyStored) {
        _id -= 4;
    } else if (_c == QMetaObject::QueryPropertyEditable) {
        _id -= 4;
    } else if (_c == QMetaObject::QueryPropertyUser) {
        _id -= 4;
    }
#endif // QT_NO_PROPERTIES
    return _id;
}

// SIGNAL 0
void VehicleStateModel::vehicleSpeedChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void VehicleStateModel::doorOpenChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void VehicleStateModel::temperatureChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}

// SIGNAL 3
void VehicleStateModel::mediaStateChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
