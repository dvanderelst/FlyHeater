/* Generated: Mon Oct 07 2019 15:53:40 GMT-0600 (Mountain Daylight Time) */

#include "device/spatialdevice.h"
static void CCONV PhidgetGyroscope_errorHandler(PhidgetChannelHandle ch, Phidget_ErrorEventCode code);
static PhidgetReturnCode CCONV PhidgetGyroscope_bridgeInput(PhidgetChannelHandle phid,
  BridgePacket *bp);
static PhidgetReturnCode CCONV PhidgetGyroscope_setStatus(PhidgetChannelHandle phid, BridgePacket *bp);
static PhidgetReturnCode CCONV PhidgetGyroscope_getStatus(PhidgetChannelHandle phid, BridgePacket **bp);
static PhidgetReturnCode CCONV PhidgetGyroscope_initAfterOpen(PhidgetChannelHandle phid);
static PhidgetReturnCode CCONV PhidgetGyroscope_setDefaults(PhidgetChannelHandle phid);
static void CCONV PhidgetGyroscope_fireInitialEvents(PhidgetChannelHandle phid);
static int CCONV PhidgetGyroscope_hasInitialState(PhidgetChannelHandle phid);

struct _PhidgetGyroscope {
	struct _PhidgetChannel phid;
	double angularRate[3];
	double minAngularRate[3];
	double maxAngularRate[3];
	int axisCount;
	uint32_t dataInterval;
	uint32_t minDataInterval;
	uint32_t maxDataInterval;
	Phidget_SpatialPrecision precision;
	double timestamp;
	PhidgetGyroscope_OnAngularRateUpdateCallback AngularRateUpdate;
	void *AngularRateUpdateCtx;
};

static PhidgetReturnCode CCONV
_setStatus(PhidgetChannelHandle phid, BridgePacket *bp) {
	PhidgetGyroscopeHandle ch;
	int version;

	ch = (PhidgetGyroscopeHandle)phid;

	version = getBridgePacketUInt32ByName(bp, "_class_version_");
	if (version != 2) {
		loginfo("%"PRIphid": server/client class version mismatch: %d != 2 - functionality may be limited.", phid, version);
	}

	if(version >= 0)
		memcpy(&ch->angularRate, getBridgePacketDoubleArrayByName(bp, "angularRate"),
	  sizeof (double) * 3);
	if(version >= 0)
		memcpy(&ch->minAngularRate, getBridgePacketDoubleArrayByName(bp, "minAngularRate"),
	  sizeof (double) * 3);
	if(version >= 0)
		memcpy(&ch->maxAngularRate, getBridgePacketDoubleArrayByName(bp, "maxAngularRate"),
	  sizeof (double) * 3);
	if(version >= 0)
		ch->axisCount = getBridgePacketInt32ByName(bp, "axisCount");
	if(version >= 0)
		ch->dataInterval = getBridgePacketUInt32ByName(bp, "dataInterval");
	if(version >= 0)
		ch->minDataInterval = getBridgePacketUInt32ByName(bp, "minDataInterval");
	if(version >= 0)
		ch->maxDataInterval = getBridgePacketUInt32ByName(bp, "maxDataInterval");
	if(version >= 2)
		ch->precision = getBridgePacketInt32ByName(bp, "precision");
	if(version >= 1)
		ch->timestamp = getBridgePacketDoubleByName(bp, "timestamp");

	return (EPHIDGET_OK);
}

static PhidgetReturnCode CCONV
_getStatus(PhidgetChannelHandle phid, BridgePacket **bp) {
	PhidgetGyroscopeHandle ch;

	ch = (PhidgetGyroscopeHandle)phid;

	return (createBridgePacket(bp, 0, "_class_version_=%u"
	  ",angularRate=%3G"
	  ",minAngularRate=%3G"
	  ",maxAngularRate=%3G"
	  ",axisCount=%d"
	  ",dataInterval=%u"
	  ",minDataInterval=%u"
	  ",maxDataInterval=%u"
	  ",precision=%d"
	  ",timestamp=%g"
	  ,2 /* class version */
	  ,ch->angularRate
	  ,ch->minAngularRate
	  ,ch->maxAngularRate
	  ,ch->axisCount
	  ,ch->dataInterval
	  ,ch->minDataInterval
	  ,ch->maxDataInterval
	  ,ch->precision
	  ,ch->timestamp
	));
}

static PhidgetReturnCode CCONV
_bridgeInput(PhidgetChannelHandle phid, BridgePacket *bp) {
	PhidgetGyroscopeHandle ch;
	PhidgetReturnCode res;

	ch = (PhidgetGyroscopeHandle)phid;
	res = EPHIDGET_OK;

	switch (bp->vpkt) {
	case BP_ZERO:
		res = DEVBRIDGEINPUT(phid, bp);
		break;
	case BP_SETDATAINTERVAL:
		TESTRANGE_IOP(bp->iop, "%"PRIu32, getBridgePacketUInt32(bp, 0), ch->minDataInterval,
		  ch->maxDataInterval);
		res = DEVBRIDGEINPUT(phid, bp);
		if (res != EPHIDGET_OK) {
			break;
		}
		ch->dataInterval = getBridgePacketUInt32(bp, 0);
		if (bridgePacketIsFromNet(bp))
			FIRE_PROPERTYCHANGE(ch, "DataInterval");
		break;
	case BP_SETSPATIALPRECISION:
		if (!supportedSpatialPrecision(phid, (Phidget_SpatialPrecision)getBridgePacketInt32(bp, 0)))
			return (MOS_ERROR(bp->iop, EPHIDGET_INVALIDARG,
			  "Specified SpatialPrecision is unsupported by this device."));
		res = DEVBRIDGEINPUT(phid, bp);
		if (res != EPHIDGET_OK) {
			break;
		}
		ch->precision = getBridgePacketInt32(bp, 0);
		if (bridgePacketIsFromNet(bp))
			FIRE_PROPERTYCHANGE(ch, "Precision");
		break;
	case BP_ANGULARRATEUPDATE:
		memcpy(&ch->angularRate, getBridgePacketDoubleArray(bp, 0), sizeof (double) * 3);
		ch->timestamp = getBridgePacketDouble(bp, 1);
		FIRECH(ch, AngularRateUpdate, ch->angularRate, ch->timestamp);
		break;
	default:
		logerr("%"PRIphid": unsupported bridge packet:0x%x", phid, bp->vpkt);
		res = EPHIDGET_UNSUPPORTED;
	}

	return (res);
}

static PhidgetReturnCode CCONV
_initAfterOpen(PhidgetChannelHandle phid) {
	PhidgetSpatialDeviceHandle parentSpatial;
	PhidgetGyroscopeHandle ch;
	PhidgetReturnCode ret;

	TESTPTR(phid);
	ch = (PhidgetGyroscopeHandle)phid;

	ret = EPHIDGET_OK;

	parentSpatial = (PhidgetSpatialDeviceHandle)phid->parent;

	switch (phid->UCD->uid) {
	case PHIDCHUID_1042_GYROSCOPE_300:
		ch->dataInterval = 256;
		ch->maxDataInterval = 1000;
		ch->maxAngularRate[0] = 2000;
		ch->maxAngularRate[1] = 2000;
		ch->maxAngularRate[2] = 2000;
		ch->minDataInterval = 4;
		ch->minAngularRate[0] = -2000;
		ch->minAngularRate[1] = -2000;
		ch->minAngularRate[2] = -2000;
		ch->angularRate[0] = parentSpatial->angularRate[ch->phid.index][0];
		ch->angularRate[1] = parentSpatial->angularRate[ch->phid.index][1];
		ch->angularRate[2] = parentSpatial->angularRate[ch->phid.index][2];
		ch->axisCount = 3;
		ch->timestamp = parentSpatial->timestamp[ch->phid.index];
		ch->precision = SPATIAL_PRECISION_LOW;
		break;
	case PHIDCHUID_1044_GYROSCOPE_400:
		ch->dataInterval = 256;
		ch->maxDataInterval = 1000;
		ch->maxAngularRate[0] = 2000;
		ch->maxAngularRate[1] = 2000;
		ch->maxAngularRate[2] = 2000;
		ch->minDataInterval = 4;
		ch->minAngularRate[0] = -2000;
		ch->minAngularRate[1] = -2000;
		ch->minAngularRate[2] = -2000;
		ch->angularRate[0] = parentSpatial->angularRate[ch->phid.index][0];
		ch->angularRate[1] = parentSpatial->angularRate[ch->phid.index][1];
		ch->angularRate[2] = parentSpatial->angularRate[ch->phid.index][2];
		ch->axisCount = 3;
		ch->timestamp = parentSpatial->timestamp[ch->phid.index];
		ch->precision = SPATIAL_PRECISION_HYBRID;
		break;
	case PHIDCHUID_1044_GYROSCOPE_500:
		ch->dataInterval = 256;
		ch->maxDataInterval = 1000;
		ch->maxAngularRate[0] = 2000;
		ch->maxAngularRate[1] = 2000;
		ch->maxAngularRate[2] = 2000;
		ch->minDataInterval = 4;
		ch->minAngularRate[0] = -2000;
		ch->minAngularRate[1] = -2000;
		ch->minAngularRate[2] = -2000;
		ch->angularRate[0] = parentSpatial->angularRate[ch->phid.index][0];
		ch->angularRate[1] = parentSpatial->angularRate[ch->phid.index][1];
		ch->angularRate[2] = parentSpatial->angularRate[ch->phid.index][2];
		ch->axisCount = 3;
		ch->timestamp = parentSpatial->timestamp[ch->phid.index];
		ch->precision = SPATIAL_PRECISION_HYBRID;
		break;
	case PHIDCHUID_1056_GYROSCOPE_000:
		ch->dataInterval = 256;
		ch->maxDataInterval = 1000;
		ch->maxAngularRate[0] = 400;
		ch->maxAngularRate[1] = 400;
		ch->maxAngularRate[2] = 400;
		ch->minDataInterval = 4;
		ch->minAngularRate[0] = -400;
		ch->minAngularRate[1] = -400;
		ch->minAngularRate[2] = -400;
		ch->angularRate[0] = parentSpatial->angularRate[ch->phid.index][0];
		ch->angularRate[1] = parentSpatial->angularRate[ch->phid.index][1];
		ch->angularRate[2] = parentSpatial->angularRate[ch->phid.index][2];
		ch->axisCount = 3;
		ch->timestamp = parentSpatial->timestamp[ch->phid.index];
		ch->precision = SPATIAL_PRECISION_HIGH;
		break;
	case PHIDCHUID_1056_GYROSCOPE_200:
		ch->dataInterval = 256;
		ch->maxDataInterval = 1000;
		ch->maxAngularRate[0] = 400;
		ch->maxAngularRate[1] = 400;
		ch->maxAngularRate[2] = 400;
		ch->minDataInterval = 4;
		ch->minAngularRate[0] = -400;
		ch->minAngularRate[1] = -400;
		ch->minAngularRate[2] = -400;
		ch->angularRate[0] = parentSpatial->angularRate[ch->phid.index][0];
		ch->angularRate[1] = parentSpatial->angularRate[ch->phid.index][1];
		ch->angularRate[2] = parentSpatial->angularRate[ch->phid.index][2];
		ch->axisCount = 3;
		ch->timestamp = parentSpatial->timestamp[ch->phid.index];
		ch->precision = SPATIAL_PRECISION_HIGH;
		break;
	case PHIDCHUID_MOT1101_GYROSCOPE_100:
		ch->dataInterval = 250;
		ch->maxDataInterval = 60000;
		ch->maxAngularRate[0] = 2000;
		ch->maxAngularRate[1] = 2000;
		ch->maxAngularRate[2] = 2000;
		ch->minDataInterval = 20;
		ch->minAngularRate[0] = -2000;
		ch->minAngularRate[1] = -2000;
		ch->minAngularRate[2] = -2000;
		ch->angularRate[0] = PUNK_DBL;
		ch->angularRate[1] = PUNK_DBL;
		ch->angularRate[2] = PUNK_DBL;
		ch->axisCount = 3;
		ch->timestamp = PUNK_DBL;
		ch->precision = SPATIAL_PRECISION_LOW;
		break;
	default:
		MOS_PANIC("Unsupported Channel");
	}


	return (ret);
}

static PhidgetReturnCode CCONV
_setDefaults(PhidgetChannelHandle phid) {
	PhidgetGyroscopeHandle ch;
	PhidgetReturnCode ret;

	TESTPTR(phid);

	ch = (PhidgetGyroscopeHandle)phid;
	ret = EPHIDGET_OK;

	switch (phid->UCD->uid) {
	case PHIDCHUID_1042_GYROSCOPE_300:
		ret = bridgeSendToDevice(phid, BP_SETDATAINTERVAL, NULL, NULL, "%u", ch->dataInterval);
		if (ret != EPHIDGET_OK) {
			break;
		}
		break;
	case PHIDCHUID_1044_GYROSCOPE_400:
		ret = bridgeSendToDevice(phid, BP_SETDATAINTERVAL, NULL, NULL, "%u", ch->dataInterval);
		if (ret != EPHIDGET_OK) {
			break;
		}
		break;
	case PHIDCHUID_1044_GYROSCOPE_500:
		ret = bridgeSendToDevice(phid, BP_SETDATAINTERVAL, NULL, NULL, "%u", ch->dataInterval);
		if (ret != EPHIDGET_OK) {
			break;
		}
		break;
	case PHIDCHUID_1056_GYROSCOPE_000:
		ret = bridgeSendToDevice(phid, BP_SETDATAINTERVAL, NULL, NULL, "%u", ch->dataInterval);
		if (ret != EPHIDGET_OK) {
			break;
		}
		break;
	case PHIDCHUID_1056_GYROSCOPE_200:
		ret = bridgeSendToDevice(phid, BP_SETDATAINTERVAL, NULL, NULL, "%u", ch->dataInterval);
		if (ret != EPHIDGET_OK) {
			break;
		}
		break;
	case PHIDCHUID_MOT1101_GYROSCOPE_100:
		ret = bridgeSendToDevice(phid, BP_SETDATAINTERVAL, NULL, NULL, "%u", ch->dataInterval);
		if (ret != EPHIDGET_OK) {
			break;
		}
		break;
	default:
		MOS_PANIC("Unsupported Channel");
	}

	return (ret);
}

static void CCONV
_fireInitialEvents(PhidgetChannelHandle phid) {
	PhidgetGyroscopeHandle ch;

	ch = (PhidgetGyroscopeHandle)phid;

	if(ch->angularRate[0] != PUNK_DBL &&
	  ch->angularRate[1] != PUNK_DBL &&
	  ch->angularRate[2] != PUNK_DBL &&
	  ch->timestamp != PUNK_DBL)
		FIRECH(ch, AngularRateUpdate, ch->angularRate, ch->timestamp);

}

static int CCONV
_hasInitialState(PhidgetChannelHandle phid) {
	PhidgetGyroscopeHandle ch;

	ch = (PhidgetGyroscopeHandle)phid;

	if(ch->angularRate[0] == PUNK_DBL ||
	  ch->angularRate[1] == PUNK_DBL ||
	  ch->angularRate[2] == PUNK_DBL ||
	  ch->timestamp == PUNK_DBL)
		return (PFALSE);

	return (PTRUE);
}

static void CCONV
PhidgetGyroscope_free(PhidgetChannelHandle *ch) {

	mos_free(*ch, sizeof (struct _PhidgetGyroscope));
}

API_PRETURN
PhidgetGyroscope_create(PhidgetGyroscopeHandle *phidp) {

	CHANNELCREATE_BODY(Gyroscope, PHIDCHCLASS_GYROSCOPE);
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_delete(PhidgetGyroscopeHandle *phidp) {

	return (Phidget_delete((PhidgetHandle *)phidp));
}

API_PRETURN
PhidgetGyroscope_zero(PhidgetGyroscopeHandle ch) {

	TESTPTR_PR(ch);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	return bridgeSendToDevice((PhidgetChannelHandle)ch, BP_ZERO, NULL, NULL, NULL);
}

API_PRETURN
PhidgetGyroscope_getAngularRate(PhidgetGyroscopeHandle ch, double (*angularRate)[3]) {

	TESTPTR_PR(ch);
	TESTPTR_PR(angularRate);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	(*angularRate)[0] = ch->angularRate[0];
	if (ch->angularRate[0] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	(*angularRate)[1] = ch->angularRate[1];
	if (ch->angularRate[1] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	(*angularRate)[2] = ch->angularRate[2];
	if (ch->angularRate[2] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_getMinAngularRate(PhidgetGyroscopeHandle ch, double (*minAngularRate)[3]) {

	TESTPTR_PR(ch);
	TESTPTR_PR(minAngularRate);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	(*minAngularRate)[0] = ch->minAngularRate[0];
	if (ch->minAngularRate[0] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	(*minAngularRate)[1] = ch->minAngularRate[1];
	if (ch->minAngularRate[1] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	(*minAngularRate)[2] = ch->minAngularRate[2];
	if (ch->minAngularRate[2] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_getMaxAngularRate(PhidgetGyroscopeHandle ch, double (*maxAngularRate)[3]) {

	TESTPTR_PR(ch);
	TESTPTR_PR(maxAngularRate);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	(*maxAngularRate)[0] = ch->maxAngularRate[0];
	if (ch->maxAngularRate[0] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	(*maxAngularRate)[1] = ch->maxAngularRate[1];
	if (ch->maxAngularRate[1] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	(*maxAngularRate)[2] = ch->maxAngularRate[2];
	if (ch->maxAngularRate[2] == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_getAxisCount(PhidgetGyroscopeHandle ch, int *axisCount) {

	TESTPTR_PR(ch);
	TESTPTR_PR(axisCount);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	*axisCount = ch->axisCount;
	if (ch->axisCount == (int)PUNK_INT32)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_setDataInterval(PhidgetGyroscopeHandle ch, uint32_t dataInterval) {

	TESTPTR_PR(ch);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	return (bridgeSendToDevice((PhidgetChannelHandle)ch, BP_SETDATAINTERVAL, NULL, NULL, "%u",
	  dataInterval));
}

API_PRETURN
PhidgetGyroscope_getDataInterval(PhidgetGyroscopeHandle ch, uint32_t *dataInterval) {

	TESTPTR_PR(ch);
	TESTPTR_PR(dataInterval);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	*dataInterval = ch->dataInterval;
	if (ch->dataInterval == (uint32_t)PUNK_UINT32)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_getMinDataInterval(PhidgetGyroscopeHandle ch, uint32_t *minDataInterval) {

	TESTPTR_PR(ch);
	TESTPTR_PR(minDataInterval);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	*minDataInterval = ch->minDataInterval;
	if (ch->minDataInterval == (uint32_t)PUNK_UINT32)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_getMaxDataInterval(PhidgetGyroscopeHandle ch, uint32_t *maxDataInterval) {

	TESTPTR_PR(ch);
	TESTPTR_PR(maxDataInterval);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	*maxDataInterval = ch->maxDataInterval;
	if (ch->maxDataInterval == (uint32_t)PUNK_UINT32)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_setPrecision(PhidgetGyroscopeHandle ch, Phidget_SpatialPrecision precision) {

	TESTPTR_PR(ch);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	return (bridgeSendToDevice((PhidgetChannelHandle)ch, BP_SETSPATIALPRECISION, NULL, NULL, "%d",
	  precision));
}

API_PRETURN
PhidgetGyroscope_getPrecision(PhidgetGyroscopeHandle ch, Phidget_SpatialPrecision *precision) {

	TESTPTR_PR(ch);
	TESTPTR_PR(precision);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	*precision = ch->precision;
	if (ch->precision == (Phidget_SpatialPrecision)PUNK_ENUM)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_getTimestamp(PhidgetGyroscopeHandle ch, double *timestamp) {

	TESTPTR_PR(ch);
	TESTPTR_PR(timestamp);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);
	TESTATTACHED_PR(ch);

	*timestamp = ch->timestamp;
	if (ch->timestamp == (double)PUNK_DBL)
		return (PHID_RETURN(EPHIDGET_UNKNOWNVAL));
	return (EPHIDGET_OK);
}

API_PRETURN
PhidgetGyroscope_setOnAngularRateUpdateHandler(PhidgetGyroscopeHandle ch,
  PhidgetGyroscope_OnAngularRateUpdateCallback fptr, void *ctx) {

	TESTPTR_PR(ch);
	TESTCHANNELCLASS_PR(ch, PHIDCHCLASS_GYROSCOPE);

	ch->AngularRateUpdate = fptr;
	ch->AngularRateUpdateCtx = ctx;

	return (EPHIDGET_OK);
}
