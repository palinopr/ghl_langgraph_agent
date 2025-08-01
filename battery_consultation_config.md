# Battery Consultation System Configuration

## Overview
This system transforms the GHL agent into a specialized battery consultation service for Puerto Rico customers, helping them find the right battery solution for power outages.

## Conversation Flow

### 1. Initial Greeting
- Agent asks if customer lives in a house or apartment
- Sets the context for battery recommendations

### 2. Equipment Assessment
- Agent asks what equipment they want to power for 6-8 hours
- Common equipment with power consumption:
  - Nevera (Refrigerator): 300W
  - TV: 70W
  - Abanico (Fan): 60W
  - Celulares (Cell phones): 15W
  - Bombilla LED (LED bulb): 10W
  - Freezer: 300W

### 3. System Recommendation
- **For Apartments**: Portable batteries that recharge via LUMA
- **For Houses**: Options include solar panels, LUMA, or generator charging

### 4. Consumption Calculation
- Uses formula: Hours = Battery Capacity (Wh) / Total Consumption (W)
- Example: 5120Wh battery / 445W consumption = ~11.5 hours

### 5. Consultation or Catalog
- If interested in consultation: Collect name, phone, email
- If not: Provide catalog link (tuplantapr.com)

## Battery Options

### Portable (Best for Apartments)
1. **EcoFlow DELTA 2** - 1024Wh - $999-$1,199
2. **Jackery Explorer 2000 Pro** - 2160Wh - $2,199-$2,499
3. **Anker PowerHouse 767** - 2048Wh - $1,999-$2,299

### High Capacity (Best for Houses)
1. **BLUETTI AC200P** - 2000Wh - $1,799-$1,999
2. **Goal Zero Yeti 3000X** - 3032Wh - $3,199-$3,499
3. **EcoFlow DELTA Pro** - 3600Wh - $3,599-$3,999

## Integration Points

### GHL Calendar Integration
- Book consultation appointments
- Send appointment confirmations
- Set reminders

### Contact Management
- Update contact with equipment preferences
- Tag as "battery-consultation"
- Add to appropriate campaigns

### Follow-up Automation
- Send battery care tips
- Seasonal reminders
- New product announcements

## Testing the System

Run the test script:
```bash
python test_battery_consultation.py
```

## Environment Variables

Add to your `.env` file:
```env
# Existing GHL configuration
GHL_API_KEY=your_key
GHL_LOCATION_ID=your_location
GHL_CALENDAR_ID=your_calendar

# Battery consultation specific
DEFAULT_CONSULTATION_DURATION=30
CATALOG_URL=https://tuplantapr.com
```

## Webhook URLs

### Meta Lead Ads
- Verification: `GET /webhook/meta`
- Lead processing: `POST /webhook/meta`

### GHL Messages
- Inbound messages: `POST /webhook/ghl`

## Deployment Notes

1. Update GHL custom fields:
   - `housing_type`: casa/apartamento
   - `equipment_list`: JSON array of equipment
   - `battery_recommendation`: Recommended model
   - `consultation_scheduled`: boolean

2. Create GHL workflows:
   - Battery consultation follow-up
   - Appointment reminder
   - Post-consultation survey

3. Set up tracking:
   - Lead source: meta-battery-ad
   - Conversion: consultation booked
   - Sale: battery purchased